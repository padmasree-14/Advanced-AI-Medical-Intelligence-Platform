import io
import base64
from typing import Tuple
from PIL import Image
import numpy as np
import cv2
import torch
import torchvision.transforms as transforms

STANDARD_IMAGE_SIZE = (224, 224)

# Standard ImageNet normalization used by EfficientNet
imagenet_normalize = transforms.Normalize(
    mean=[0.485, 0.456, 0.406],
    std=[0.229, 0.224, 0.225]
)

transform_pipeline = transforms.Compose([
    transforms.Resize(STANDARD_IMAGE_SIZE),
    transforms.ToTensor(),
    imagenet_normalize
])

def load_and_preprocess_image(image_bytes: bytes) -> Tuple[Image.Image, torch.Tensor, np.ndarray]:
    """
    Loads raw image bytes and returns:
    1. PIL RGB Image
    2. PyTorch tensor ready for model input (shape: 1, 3, 224, 224)
    3. OpenCV BGR numpy array for OpenCV Grad-CAM visualization
    """
    pil_img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    
    # PyTorch Tensor transform
    tensor_img = transform_pipeline(pil_img).unsqueeze(0)  # Add batch dimension
    
    # OpenCV format (BGR array)
    cv2_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    cv2_img = cv2.resize(cv2_img, STANDARD_IMAGE_SIZE)
    
    return pil_img, tensor_img, cv2_img

def numpy_to_base64(img_bgr: np.ndarray, format: str = ".jpg") -> str:
    """Encodes OpenCV BGR image array into base64 data URL string."""
    _, buffer = cv2.imencode(format, img_bgr)
    b64_str = base64.b64encode(buffer).decode("utf-8")
    return f"data:image/jpeg;base64,{b64_str}"

def bytes_to_base64(image_bytes: bytes, mime_type: str = "image/jpeg") -> str:
    b64_str = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:{mime_type};base64,{b64_str}"
