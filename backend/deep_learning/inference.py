import os
import logging
from typing import Dict, Any, List, Tuple
import torch
import torch.nn.functional as F

from backend.config.settings import settings
from backend.deep_learning.model import MedicalEfficientNet, MEDICAL_CLASSES

logger = logging.getLogger(__name__)

class DeepLearningEngine:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model: MedicalEfficientNet = None
        self.classes = MEDICAL_CLASSES
        self._load_model()

    def _load_model(self):
        try:
            logger.info(f"Initializing Medical EfficientNet-B0 model on device: {self.device}")
            self.model = MedicalEfficientNet(num_classes=len(self.classes), pretrained=True)
            
            # Check if custom fine-tuned weights exist
            model_path = settings.MODEL_PATH
            if os.path.exists(model_path):
                logger.info(f"Loading custom fine-tuned weights from {model_path}...")
                state_dict = torch.load(model_path, map_location=self.device)
                self.model.load_state_dict(state_dict)
            else:
                logger.info("Custom weights file not found. Running with initialized pre-trained transfer learning weights.")
            
            self.model.to(self.device)
            self.model.eval()
            logger.info("Medical EfficientNet-B0 model ready for inference.")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise e

    def predict(self, tensor_img: torch.Tensor) -> Dict[str, Any]:
        """
        Runs model inference on input image tensor.
        Returns:
            Dict containing predicted_class, confidence, all_probabilities (sorted).
        """
        tensor_img = tensor_img.to(self.device)
        with torch.no_grad():
            outputs = self.model(tensor_img)
            probabilities = F.softmax(outputs, dim=1)[0]
            
        prob_list: List[Tuple[str, float]] = []
        for i, cls_name in enumerate(self.classes):
            prob_list.append((cls_name, float(probabilities[i].item())))
        
        # Sort descending
        prob_list.sort(key=lambda x: x[1], reverse=True)
        top_class, top_conf = prob_list[0]
        
        return {
            "predicted_class": top_class,
            "confidence": round(top_conf * 100, 2),
            "all_probabilities": [
                {"class_name": cls, "confidence": round(conf * 100, 2)}
                for cls, conf in prob_list
            ]
        }

dl_engine = DeepLearningEngine()
