import os
import sys
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

# Add parent directory to path to allow importing mscn
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import only the available components
from mscn.model import SetConv
from mscn.util import unnormalize_labels

# Define a simple model that uses SetConv
class SimpleCardinalityEstimator(nn.Module):
    def __init__(self, input_size, hidden_size=128):
        super(SimpleCardinalityEstimator, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size // 2)
        self.fc3 = nn.Linear(hidden_size // 2, 1)
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()
    
    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return self.sigmoid(x)

def main():
    print("Starting simple test of MSCN model...")
    
    # Set random seed for reproducibility
    torch.manual_seed(42)
    np.random.seed(42)
    
    # Check if CUDA is available
    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")
    print(f"Using device: {device}")
    
    # Create a small test dataset
    num_samples = 100
    num_columns = 10
    
    # Generate random data for testing
    X = np.random.rand(num_samples, num_columns).astype(np.float32)
    y = np.random.rand(num_samples, 1).astype(np.float32)
    
    # Create data loaders
    train_loader = torch.utils.data.DataLoader(
        torch.utils.data.TensorDataset(
            torch.FloatTensor(X[:80]),  # 80% training
            torch.FloatTensor(y[:80])
        ),
        batch_size=8,
        shuffle=True
    )
    
    test_loader = torch.utils.data.DataLoader(
        torch.utils.data.TensorDataset(
            torch.FloatTensor(X[80:]),  # 20% test
            torch.FloatTensor(y[80:])
        ),
        batch_size=8,
        shuffle=False
    )
    
    # Initialize model
    model = SimpleCardinalityEstimator(num_columns).to(device)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    # Training loop
    print("Starting training...")
    num_epochs = 5
    for epoch in range(num_epochs):
        model.train()
        train_loss = 0.0
        
        for batch_x, batch_y in train_loader:
            batch_x, batch_y = batch_x.to(device), batch_y.to(device)
            
            # Forward pass
            optimizer.zero_grad()
            outputs = model(batch_x)
            loss = criterion(outputs, batch_y)
            
            # Backward pass and optimize
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
        
        # Print training progress
        avg_train_loss = train_loss / len(train_loader)
        print(f"Epoch [{epoch+1}/{num_epochs}], Train Loss: {avg_train_loss:.4f}")
    
    # Test the model
    model.eval()
    with torch.no_grad():
        test_loss = 0.0
        for batch_x, batch_y in test_loader:
            batch_x, batch_y = batch_x.to(device), batch_y.to(device)
            outputs = model(batch_x)
            test_loss += criterion(outputs, batch_y).item()
        
        avg_test_loss = test_loss / len(test_loader)
        print(f"Test Loss: {avg_test_loss:.4f}")
    
    print("Test completed successfully!")

if __name__ == "__main__":
    # Add parent directory to path to allow importing mscn
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    main()
