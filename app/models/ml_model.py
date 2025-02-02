from abc import ABC, abstractmethod


class MLModel(ABC):
    @abstractmethod
    def predict(self, image_path: str) -> str:
        pass


class ResNet50Model(MLModel):
    def predict(self, image_path: str) -> str:
        return "Dog"
