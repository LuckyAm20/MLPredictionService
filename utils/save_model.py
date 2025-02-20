import torch
import torchvision.models as models

model = models.resnet50(pretrained=True)

model.eval()
torch.save(model, "resnet50.pth")


model = models.efficientnet_b0(pretrained=True)
model.eval()

torch.save(model, "../models/efficientnet_b0.pth")
