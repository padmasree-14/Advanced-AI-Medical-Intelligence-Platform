import cv2
import numpy as np
import torch
import torch.nn.functional as F
from backend.utils.image_processing import numpy_to_base64

class GradCAMExplainer:
    """
    Grad-CAM Explainer for PyTorch EfficientNet-B0 Medical Image Visual Diagnostics.
    """
    def __init__(self, model, target_layer):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None
        self._register_hooks()

    def _register_hooks(self):
        def forward_hook(module, input, output):
            self.activations = output.detach()

        def backward_hook(module, grad_in, grad_out):
            self.gradients = grad_out[0].detach()

        self.target_layer.register_forward_hook(forward_hook)
        self.target_layer.register_full_backward_hook(backward_hook)

    def generate_heatmap(
        self,
        tensor_img: torch.Tensor,
        cv2_img_bgr: np.ndarray,
        target_class_idx: int = None,
        alpha: float = 0.5
    ) -> str:
        """
        Generates Grad-CAM visual heatmap overlay over input image.
        Returns:
            base64 data URL string of the heatmap overlay image.
        """
        self.model.eval()
        tensor_img = tensor_img.to(next(self.model.parameters()).device)
        tensor_img.requires_grad_(True)

        # Forward pass
        output = self.model(tensor_img)

        if target_class_idx is None:
            target_class_idx = torch.argmax(output, dim=1).item()

        score = output[0, target_class_idx]

        # Zero existing gradients and backward pass
        self.model.zero_grad()
        score.backward(retain_graph=True)

        # Retrieve gradients and activations from target layer
        gradients = self.gradients[0].cpu().data.numpy()      # shape (C, H, W)
        activations = self.activations[0].cpu().data.numpy()  # shape (C, H, W)

        # Global average pooling on gradients to calculate channel importance weights
        weights = np.mean(gradients, axis=(1, 2))              # shape (C,)

        # Compute weighted sum of feature maps
        cam = np.zeros(activations.shape[1:], dtype=np.float32)
        for i, w in enumerate(weights):
            cam += w * activations[i, :, :]

        # Apply ReLU to focus on positive influences
        cam = np.maximum(cam, 0)

        # Resize CAM to original image dimensions
        h, w, _ = cv2_img_bgr.shape
        if np.max(cam) != 0:
            cam = cam / np.max(cam)  # Normalize between 0 and 1
        cam = cv2.resize(cam, (w, h))

        # Convert to 8-bit heatmap image with JET colormap
        heatmap = np.uint8(255 * cam)
        heatmap_colored = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

        # Superimpose heatmap on original image
        overlay = cv2.addWeighted(cv2_img_bgr, 1 - alpha, heatmap_colored, alpha, 0)

        return numpy_to_base64(overlay)
