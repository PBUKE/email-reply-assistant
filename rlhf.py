import torch
import torch.nn as nn
import torch.optim as optim
from torch.distributions import Categorical
import numpy as np
from tqdm import tqdm

class PPOTrainer:
    def __init__(self, model, reward_function, learning_rate=1e-5, epsilon=0.2):
        self.model = model
        self.reward_function = reward_function
        self.optimizer = optim.Adam(model.parameters(), lr=learning_rate)
        self.epsilon = epsilon  # PPO clipping parameter
        
    def compute_advantages(self, rewards, values, gamma=0.99, lambda_=0.95):
        """Compute Generalized Advantage Estimation (GAE)."""
        advantages = []
        gae = 0
        
        for t in reversed(range(len(rewards))):
            if t == len(rewards) - 1:
                next_value = 0
            else:
                next_value = values[t + 1]
                
            delta = rewards[t] + gamma * next_value - values[t]
            gae = delta + gamma * lambda_ * gae
            advantages.insert(0, gae)
            
        return torch.tensor(advantages)

    def train_step(self, email_text, num_iterations=5):
        """Perform one training step using PPO."""
        # Generate initial reply and get its reward
        original_reply = self.model.generate_reply(email_text)
        original_scores = self.reward_function.calculate_total_score(original_reply)
        original_reward = original_scores['total_score']
        
        # Get model's current policy probabilities
        inputs = self.model.tokenizer(email_text, return_tensors="pt").to(self.model.device)
        with torch.no_grad():
            outputs = self.model.model(**inputs)
            old_logits = outputs.logits
            old_probs = torch.softmax(old_logits, dim=-1)
        
        # PPO training loop
        for _ in range(num_iterations):
            # Forward pass with new parameters
            outputs = self.model.model(**inputs)
            new_logits = outputs.logits
            new_probs = torch.softmax(new_logits, dim=-1)
            
            # Calculate ratio of new and old probabilities
            ratio = (new_probs / (old_probs + 1e-10))
            
            # Calculate surrogate losses
            surrogate1 = ratio * original_reward
            surrogate2 = torch.clamp(ratio, 1 - self.epsilon, 1 + self.epsilon) * original_reward
            
            # PPO loss
            loss = -torch.min(surrogate1, surrogate2).mean()
            
            # Update model
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
    
    def train(self, training_data, epochs=3):
        """Train the model using PPO on a dataset of emails."""
        self.model.model.train()
        
        for epoch in range(epochs):
            total_reward = 0
            progress_bar = tqdm(training_data, desc=f"Epoch {epoch+1}/{epochs}")
            
            for email_text in progress_bar:
                # Train on single example
                self.train_step(email_text)
                
                # Generate reply and get reward for progress tracking
                with torch.no_grad():
                    reply = self.model.generate_reply(email_text)
                    scores = self.reward_function.calculate_total_score(reply)
                    total_reward += scores['total_score']
                
                # Update progress bar
                progress_bar.set_postfix({
                    'avg_reward': f"{total_reward / (progress_bar.n + 1):.3f}"
                })
            
        self.model.model.eval() 