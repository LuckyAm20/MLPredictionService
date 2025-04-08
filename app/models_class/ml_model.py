from abc import ABC, abstractmethod

import torch
from torchvision import transforms


class MLModel(ABC):
    def __init__(self, model):
        self.model = model
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
        ])

    def predict(self, image) -> int:
        with torch.no_grad():
            output = self.model(image)
            predicted_class = output.argmax().item()
        return predicted_class


class ResNet50Model(MLModel):
    def predict(self, image_path: str) -> str:
        return "Dog"
