"""
Simple training script for DouZero - single process, single thread, CPU only
"""
import torch
from torch import nn
import numpy as np
from torch.utils.data import DataLoader, TensorDataset

from src.model.LandlordModel import CLandlordLstmModel
from src.model.FamerModel import CFarmerLstmModel
from src.base_element.Role import CRole


def create_models(device='cpu'):
    """Create models for each position"""
    return {
        CRole.LANDLORD: CLandlordLstmModel().to(device),
        CRole.LANDLORD_UP: CFarmerLstmModel().to(device),
        CRole.LANDLORD_DOWN: CFarmerLstmModel().to(device)
    }


def create_optimizers(models, learning_rate=1e-4):
    """Create optimizers for each model"""
    return {
        role: torch.optim.Adam(model.parameters(), lr=learning_rate)
        for role, model in models.items()
    }


def compute_loss(logits, targets):
    """Compute MSE loss between predictions and targets"""
    return ((logits.squeeze(-1) - targets) ** 2).mean()


def learn_step(position, model, optimizer, obs_z, obs_x, targets, losses):
    """
    Perform one learning step for a specific position
    """
    device = next(model.parameters()).device
    obs_z = obs_z.to(device)
    obs_x = obs_x.to(device)
    targets = targets.to(device)

    # Forward pass
    outputs = model(obs_z, obs_x, return_value=True)
    loss = compute_loss(outputs['values'], targets)
    
    # Backward pass
    optimizer.zero_grad()
    loss.backward()
    nn.utils.clip_grad_norm_(model.parameters(), max_norm=40.0)
    optimizer.step()
    
    # Record statistics
    losses[position].append(loss.item())


def create_dummy_batch(num_samples=256, seq_len=5):
    """
    Create dummy batch data for demonstration
    In a real scenario, this would come from game play
    """
    datasets = {}
    for role in [CRole.LANDLORD, CRole.LANDLORD_UP, CRole.LANDLORD_DOWN]:
        x_dim = 304 if role == CRole.LANDLORD else 307
        obs_z = torch.randn(num_samples, seq_len, 162)
        obs_x = torch.randn(num_samples, x_dim)
        target = torch.randn(num_samples)
        datasets[role] = TensorDataset(obs_z, obs_x, target)
    return datasets


def train(total_episodes=1000, learning_rate=1e-4, batch_size=32):
    """
    Main training loop
    
    Args:
        total_episodes: Number of training episodes
        learning_rate: Learning rate for optimizer
        batch_size: Batch size for training
    """
    # Init model and optimizer
    device = torch.device('cpu')
    models = create_models(device=device) # 似乎不太对
    optimizers = create_optimizers(models, learning_rate=learning_rate)
    losses = {role: [] for role in models.keys()}
    
    # Training loop
    for episode in range(total_episodes):
        # Create role-wise datasets (in real scenario, collect from game play)
        datasets = create_dummy_batch(num_samples=max(batch_size * 4, 1))
        
        # Train each position
        for role in models.keys():
            loader = DataLoader(datasets[role], batch_size=batch_size, shuffle=True)
            for role_obs_z, role_obs_x, role_target in loader:
                learn_step(
                    position=role,
                    model=models[role],
                    optimizer=optimizers[role],
                    obs_z=role_obs_z,
                    obs_x=role_obs_x,
                    targets=role_target,
                    losses=losses
                )
    
    print("\n=== Training Completed ===")
    print("Final Statistics:")
    for role in models.keys():
        avg_loss = np.mean(losses[role][-100:]) if losses[role] else 0
        print(f"{role.name}: Loss={avg_loss:.4f}")
    
    return models


def main():
    """Entry point for training"""
    train(total_episodes=1000, learning_rate=1e-4, batch_size=32)


if __name__ == '__main__':
    main()
