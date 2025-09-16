import torch
import torch.nn as nn
import torch.nn.functional as F
from pathlib import Path

# ----------------------
# Model Architecture
# ----------------------
class MyModel(nn.Module):
    def __init__(self, num_classes=3):
        super(MyModel, self).__init__()
        # Convolutional Block 1
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(32)
        self.pool1 = nn.MaxPool2d(2, 2)

        # Convolutional Block 2
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(64)
        self.pool2 = nn.MaxPool2d(2, 2)

        # Convolutional Block 3
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm2d(128)
        self.pool3 = nn.MaxPool2d(2, 2)

        # Global average pooling
        self.global_pool = nn.AdaptiveAvgPool2d(1)
        self.flatten = nn.Flatten()

        # Fully connected layers
        self.fc1 = nn.Linear(128, 128)
        self.bn_fc1 = nn.BatchNorm1d(128)
        self.dropout = nn.Dropout(0.5)
        self.fc2 = nn.Linear(128, num_classes)

    def forward(self, x):
        x = F.relu(self.bn1(self.conv1(x)))
        x = self.pool1(x)

        x = F.relu(self.bn2(self.conv2(x)))
        x = self.pool2(x)

        x = F.relu(self.bn3(self.conv3(x)))
        x = self.pool3(x)

        x = self.global_pool(x)
        x = self.flatten(x)

        embed = self.fc1(x)  
        x = F.relu(self.bn_fc1(embed))
        x = self.dropout(x)
        x = self.fc2(x)
        return x, embed  # logits + embeddings


# ----------------------
# Model Loader
# ----------------------
def load_model(model_path: str = "model/best_model.pth", device=None) -> MyModel:
    """
    Load the trained model for inference.
    """
    if device is None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = MyModel().to(device)

    model_file = Path(model_path)
    if not model_file.exists():
        raise FileNotFoundError(f"Model file not found at {model_file.resolve()}")

    state_dict = torch.load(model_file, map_location=device)
    model.load_state_dict(state_dict)
    model.eval()
    return model
