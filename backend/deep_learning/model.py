import torch
import torch.nn as nn
from torchvision.models import efficientnet_b0, EfficientNet_B0_Weights

MEDICAL_CLASSES = ["Normal", "Pneumonia", "Tuberculosis", "COVID-19"]

class MedicalEfficientNet(nn.Module):
    """
    EfficientNet-B0 Neural Network fine-tuned for multi-class Medical Diagnostic Imaging.
    Feature extractor layer is accessible for Grad-CAM activations via `model.model.features`.
    """
    def __init__(self, num_classes: int = len(MEDICAL_CLASSES), pretrained: bool = True):
        super(MedicalEfficientNet, self).__init__()
        weights = EfficientNet_B0_Weights.DEFAULT if pretrained else None
        self.model = efficientnet_b0(weights=weights)
        
        # Replace classifier head for target medical classes
        in_features = self.model.classifier[1].in_features
        self.model.classifier = nn.Sequential(
            nn.Dropout(p=0.3, inplace=True),
            nn.Linear(in_features, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(),
            nn.Dropout(p=0.2),
            nn.Linear(512, num_classes)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.model(x)

    def get_target_layer(self):
        """Returns the final convolutional feature layer of EfficientNet-B0 for Grad-CAM."""
        return self.model.features[-1]
