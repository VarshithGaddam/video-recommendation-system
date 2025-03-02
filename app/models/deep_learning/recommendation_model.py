import torch
import torch.nn as nn
import torch.nn.functional as F

class VideoRecommenderDNN(nn.Module):
    def __init__(
        self,
        num_users,
        num_videos,
        embedding_dim=128,
        hidden_layers=[256, 128, 64],
        dropout_rate=0.3
    ):
        super(VideoRecommenderDNN, self).__init__()
        
        # Embedding layers
        self.user_embedding = nn.Embedding(num_users, embedding_dim)
        self.video_embedding = nn.Embedding(num_videos, embedding_dim)
        
        # Create stack of dense layers
        layers = []
        input_dim = embedding_dim * 2  # Concatenated embeddings
        
        for hidden_dim in hidden_layers:
            layers.extend([
                nn.Linear(input_dim, hidden_dim),
                nn.ReLU(),
                nn.Dropout(dropout_rate)
            ])
            input_dim = hidden_dim
        
        self.dense_layers = nn.Sequential(*layers)
        
        # Output layer
        self.output_layer = nn.Linear(hidden_layers[-1], 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, user_ids, video_ids):
        # Ensure inputs are properly shaped tensors
        if not isinstance(user_ids, torch.Tensor):
            user_ids = torch.tensor(user_ids, dtype=torch.long)
        if not isinstance(video_ids, torch.Tensor):
            video_ids = torch.tensor(video_ids, dtype=torch.long)
        
        # Reshape inputs if necessary
        if user_ids.dim() == 1:
            user_ids = user_ids.unsqueeze(0)
        if video_ids.dim() == 1:
            video_ids = video_ids.unsqueeze(0)
            
        # Expand user_ids to match video_ids size
        if user_ids.size(0) == 1 and video_ids.size(0) > 1:
            user_ids = user_ids.expand(video_ids.size(0), -1)
        
        # Get embeddings
        user_embedded = self.user_embedding(user_ids).squeeze(1)
        video_embedded = self.video_embedding(video_ids).squeeze(1)
        
        # Concatenate embeddings
        concatenated = torch.cat([user_embedded, video_embedded], dim=1)
        
        # Pass through dense layers
        x = self.dense_layers(concatenated)
        
        # Get prediction
        output = self.output_layer(x)
        prediction = self.sigmoid(output)
        
        return prediction

    def get_user_embedding(self, user_id):
        if not isinstance(user_id, torch.Tensor):
            user_id = torch.tensor([user_id], dtype=torch.long)
        return self.user_embedding(user_id)

    def get_video_embedding(self, video_id):
        if not isinstance(video_id, torch.Tensor):
            video_id = torch.tensor([video_id], dtype=torch.long)
        return self.video_embedding(video_id)