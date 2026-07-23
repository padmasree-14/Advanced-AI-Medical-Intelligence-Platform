import os
import sys
import torch
import numpy as np
from torch.utils.data import DataLoader
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, roc_auc_score, confusion_matrix

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.deep_learning.model import MedicalEfficientNet, MEDICAL_CLASSES
from training.dataset import MedicalDataset
from training.prepare_dataset import generate_dataset

def evaluate_model(
    data_dir: str = os.path.join("data", "medical_images"),
    model_path: str = os.path.join("models", "efficientnet_b0_medical.pth")
):
    if not os.path.exists(data_dir):
        generate_dataset()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    test_dataset = MedicalDataset(data_dir=data_dir, split="test")
    test_loader = DataLoader(test_dataset, batch_size=8, shuffle=False)

    model = MedicalEfficientNet(num_classes=len(MEDICAL_CLASSES), pretrained=True)
    if os.path.exists(model_path):
        model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()

    all_preds = []
    all_targets = []
    all_probs = []

    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(device)
            outputs = model(images)
            probs = torch.softmax(outputs, dim=1)
            _, preds = torch.max(outputs, 1)

            all_preds.extend(preds.cpu().numpy())
            all_targets.extend(labels.numpy())
            all_probs.extend(probs.cpu().numpy())

    all_preds = np.array(all_preds)
    all_targets = np.array(all_targets)
    all_probs = np.array(all_probs)

    acc = accuracy_score(all_targets, all_preds)
    precision, recall, f1, _ = precision_recall_fscore_support(all_targets, all_preds, average='weighted', zero_division=0)
    
    try:
        roc_auc = roc_auc_score(all_targets, all_probs, multi_class='ovr')
    except Exception:
        roc_auc = 0.0

    cm = confusion_matrix(all_targets, all_preds)

    print("\n" + "="*50)
    print("      EFFICIENTNET-B0 MEDICAL MODEL EVALUATION")
    print("="*50)
    print(f"Accuracy : {acc * 100:.2f}%")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1-Score : {f1:.4f}")
    print(f"ROC-AUC  : {roc_auc:.4f}")
    print("\nConfusion Matrix:")
    print(cm)
    print("="*50 + "\n")

    return {
        "accuracy": acc,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "roc_auc": roc_auc,
        "confusion_matrix": cm.tolist()
    }

if __name__ == "__main__":
    evaluate_model()
