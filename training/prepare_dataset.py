import os
import numpy as np
import cv2
from PIL import Image, ImageDraw

DATASET_DIR = os.path.join("data", "medical_images")
CLASSES = ["Normal", "Pneumonia", "Tuberculosis", "COVID-19"]

def create_synthetic_xray(class_name: str, index: int) -> np.ndarray:
    """
    Generates a realistic synthetic chest radiograph pattern for model training/testing.
    """
    img_size = (224, 224)
    # Base ribcage/lung shadow background (dark gray with lung contours)
    base = np.full((224, 224, 3), 30, dtype=np.uint8)
    
    # Left and right lung field ellipses
    cv2.ellipse(base, (75, 110), (35, 75), 0, 0, 360, (120, 120, 120), -1)
    cv2.ellipse(base, (149, 110), (35, 75), 0, 0, 360, (120, 120, 120), -1)
    
    # Spine/mediastinum central shadow
    cv2.rectangle(base, (102, 30), (122, 190), (180, 180, 180), -1)
    # Heart shadow (left-sided blur)
    cv2.ellipse(base, (125, 130), (25, 30), 20, 0, 360, (190, 190, 190), -1)

    # Class-specific diagnostic visual features
    np.random.seed(index * 7 + len(class_name))
    if class_name == "Pneumonia":
        # Dense patchy opacity in lower right lung field
        cv2.circle(base, (70, 140), 22, (230, 230, 230), -1)
        base = cv2.GaussianBlur(base, (15, 15), 0)
    elif class_name == "Tuberculosis":
        # Apical cavitary lesion in upper right lung field
        cv2.circle(base, (75, 65), 16, (240, 240, 240), -1)
        cv2.circle(base, (75, 65), 8, (60, 60, 60), -1) # cavitary center
        base = cv2.GaussianBlur(base, (7, 7), 0)
    elif class_name == "COVID-19":
        # Bilateral peripheral ground-glass opacities
        cv2.ellipse(base, (50, 120), (12, 35), 0, 0, 360, (210, 210, 210), -1)
        cv2.ellipse(base, (174, 120), (12, 35), 0, 0, 360, (210, 210, 210), -1)
        base = cv2.GaussianBlur(base, (11, 11), 0)
    else: # Normal
        base = cv2.GaussianBlur(base, (5, 5), 0)

    # Add subtle radiographic noise
    noise = np.random.normal(0, 8, base.shape).astype(np.uint8)
    img_noisy = cv2.add(base, noise)
    return img_noisy

def generate_dataset(samples_per_class: int = 40):
    print("Generating synthetic Chest Radiograph dataset for pipeline verification...")
    for split in ["train", "val", "test"]:
        split_count = int(samples_per_class * (0.7 if split == "train" else 0.15))
        for cls in CLASSES:
            dir_path = os.path.join(DATASET_DIR, split, cls)
            os.makedirs(dir_path, exist_ok=True)
            for i in range(split_count):
                img_array = create_synthetic_xray(cls, i)
                file_path = os.path.join(dir_path, f"{cls.lower()}_{split}_{i+1}.jpg")
                cv2.imwrite(file_path, img_array)
    print(f"Dataset generated under '{DATASET_DIR}'.")

if __name__ == "__main__":
    generate_dataset()
