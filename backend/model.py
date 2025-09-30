import torch
import torch.nn as nn
import timm
from utils import process_image

MODEL_PATH = "./models/best_model_convnext_v2.pth"

class ConvNeXtSingleFrame(nn.Module):
    def __init__(self, num_classes=7):
        super().__init__()
        base_model = timm.create_model('convnext_base', pretrained=True, num_classes=0) 
        self.backbone = base_model
        self.dropout = nn.Dropout(0.5)
        self.fc = nn.Linear(1024, num_classes)

    def forward(self, x):
        x = self.backbone(x)
        x = self.dropout(x)
        return self.fc(x)

def load_model():
    model = ConvNeXtSingleFrame(num_classes=7)
    state_dict = torch.load(MODEL_PATH, map_location="cpu")
    model.load_state_dict(state_dict)
    model.eval()
    return model

def predict(model, image_bytes):
    tensor = process_image(image_bytes)
    with torch.no_grad():
        outputs = model(tensor)
        _, predicted = outputs.max(1)

    classes = ["ORIGINAL", "FACE2FACE", "FACESHIFTER", "FACESWAP", "DEEPFAKEDETECTION", "DEEPFAKES", "NEURALTEXTURES"]

    result = classes[predicted.item()]
    explanation = f"Classificada como {result} pelo modelo ConvNeXt."
    return result, explanation
