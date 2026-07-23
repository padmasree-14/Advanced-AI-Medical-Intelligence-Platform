import os
from typing import Tuple, List, Optional
from PIL import Image
import torch
from torch.utils.data import Dataset
import torchvision.transforms as transforms

CLASSES = ["Normal", "Pneumonia", "Tuberculosis", "COVID-19"]

def get_data_transforms(split: str = "train") -> transforms.Compose:
    mean = [0.485, 0.456, 0.406]
    std = [0.229, 0.224, 0.225]
    
    if split == "train":
        return transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.RandomRotation(degrees=10),
            transforms.RandomHorizontalFlip(p=0.3),
            transforms.ColorJitter(brightness=0.1, contrast=0.1),
            transforms.ToTensor(),
            transforms.Normalize(mean=mean, std=std)
        ])
    else:
        return transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=mean, std=std)
        ])

class MedicalDataset(Dataset):
    """
    PyTorch Dataset for Medical Image Classification.
    """
    def __init__(self, data_dir: str, split: str = "train", transform: Optional[transforms.Compose] = None):
        self.data_dir = os.path.join(data_dir, split)
        self.classes = CLASSES
        self.class_to_idx = {cls: idx for idx, cls in enumerate(self.classes)}
        self.samples: List[Tuple[str, int]] = []
        self.transform = transform or get_data_transforms(split)

        if os.path.exists(self.data_dir):
            for cls in self.classes:
                cls_folder = os.path.join(self.data_dir, cls)
                if os.path.isdir(cls_folder):
                    for fname in os.listdir(cls_folder):
                        if fname.lower().endswith(('.jpg', '.jpeg', '.png')):
                            self.samples.append((os.path.join(cls_folder, fname), self.class_to_idx[cls]))

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, int]:
        img_path, label = self.samples[idx]
        image = Image.open(img_path).convert("RGB")
        if self.transform:
            image = self.transform(image)
        return image, label
