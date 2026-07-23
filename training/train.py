import os
import sys
import time
import logging
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

# Add root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.deep_learning.model import MedicalEfficientNet, MEDICAL_CLASSES
from training.dataset import MedicalDataset, get_data_transforms
from training.prepare_dataset import generate_dataset

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class EarlyStopping:
    def __init__(self, patience: int = 5, delta: float = 0.001):
        self.patience = patience
        self.delta = delta
        self.counter = 0
        self.best_loss = None
        self.early_stop = False

    def __call__(self, val_loss: float) -> bool:
        if self.best_loss is None:
            self.best_loss = val_loss
        elif val_loss > self.best_loss - self.delta:
            self.counter += 1
            logger.info(f"EarlyStopping counter: {self.counter} out of {self.patience}")
            if self.counter >= self.patience:
                self.early_stop = True
        else:
            self.best_loss = val_loss
            self.counter = 0
        return self.early_stop

def train_model(
    data_dir: str = os.path.join("data", "medical_images"),
    output_model_path: str = os.path.join("models", "efficientnet_b0_medical.pth"),
    epochs: int = 10,
    batch_size: int = 8,
    lr: float = 1e-3
):
    # Ensure dataset exists
    if not os.path.exists(data_dir):
        logger.info("Dataset directory not found. Generating synthetic dataset for verification...")
        generate_dataset(samples_per_class=40)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logger.info(f"Training EfficientNet-B0 on device: {device}")

    # Datasets & Dataloaders
    train_dataset = MedicalDataset(data_dir=data_dir, split="train")
    val_dataset = MedicalDataset(data_dir=data_dir, split="val")

    if len(train_dataset) == 0:
        logger.warning("Empty training dataset. Re-generating dataset...")
        generate_dataset(samples_per_class=40)
        train_dataset = MedicalDataset(data_dir=data_dir, split="train")
        val_dataset = MedicalDataset(data_dir=data_dir, split="val")

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

    model = MedicalEfficientNet(num_classes=len(MEDICAL_CLASSES), pretrained=True).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=2)
    early_stopping = EarlyStopping(patience=5)

    os.makedirs(os.path.dirname(output_model_path), exist_ok=True)
    best_acc = 0.0

    for epoch in range(epochs):
        start_t = time.time()
        # Train phase
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * images.size(0)
            _, preds = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (preds == labels).sum().item()

        epoch_train_loss = running_loss / (total if total > 0 else 1)
        epoch_train_acc = (correct / total) * 100 if total > 0 else 0.0

        # Validation phase
        model.eval()
        val_loss = 0.0
        val_correct = 0
        val_total = 0

        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                loss = criterion(outputs, labels)

                val_loss += loss.item() * images.size(0)
                _, preds = torch.max(outputs, 1)
                val_total += labels.size(0)
                val_correct += (preds == labels).sum().item()

        epoch_val_loss = val_loss / (val_total if val_total > 0 else 1)
        epoch_val_acc = (val_correct / val_total) * 100 if val_total > 0 else 0.0

        scheduler.step(epoch_val_loss)

        elapsed = time.time() - start_t
        logger.info(
            f"Epoch [{epoch+1}/{epochs}] ({elapsed:.1f}s) - "
            f"Train Loss: {epoch_train_loss:.4f}, Train Acc: {epoch_train_acc:.2f}% | "
            f"Val Loss: {epoch_val_loss:.4f}, Val Acc: {epoch_val_acc:.2f}%"
        )

        # Save best model
        if epoch_val_acc >= best_acc:
            best_acc = epoch_val_acc
            torch.save(model.state_dict(), output_model_path)
            logger.info(f"--> Saved updated best model checkpoint to {output_model_path}")

        if early_stopping(epoch_val_loss):
            logger.info("Early stopping threshold reached. Terminating training loop.")
            break

    logger.info(f"Training completed. Best Validation Accuracy: {best_acc:.2f}%")

if __name__ == "__main__":
    train_model(epochs=5)
