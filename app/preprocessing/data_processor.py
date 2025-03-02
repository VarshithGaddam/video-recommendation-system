import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from typing import Dict, List, Tuple

class DataPreprocessor:
    def __init__(self):
        self.user_encoder = LabelEncoder()
        self.video_encoder = LabelEncoder()
        self.feature_scaler = StandardScaler()
        self.categorical_encoders: Dict[str, LabelEncoder] = {}
        
    def preprocess_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess features including normalization and encoding
        """
        # Create copy to avoid modifying original data
        df_processed = df.copy()
        
        # Handle missing values
        df_processed = self._handle_missing_values(df_processed)
        
        # Encode categorical variables
        categorical_columns = df_processed.select_dtypes(include=['object']).columns
        for col in categorical_columns:
            if col not in self.categorical_encoders:
                self.categorical_encoders[col] = LabelEncoder()
            df_processed[col] = self.categorical_encoders[col].fit_transform(df_processed[col])
        
        # Normalize numerical features
        numerical_columns = df_processed.select_dtypes(include=['float64', 'int64']).columns
        df_processed[numerical_columns] = self.feature_scaler.fit_transform(df_processed[numerical_columns])
        
        return df_processed
    
    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Handle missing values in the dataset
        """
        # Fill numeric columns with median
        numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
        for col in numeric_columns:
            df[col] = df[col].fillna(df[col].median())
        
        # Fill categorical columns with mode
        categorical_columns = df.select_dtypes(include=['object']).columns
        for col in categorical_columns:
            df[col] = df[col].fillna(df[col].mode()[0])
            
        return df
    
    def prepare_mood_features(self, mood: str) -> np.ndarray:
        """
        Process mood-based features for cold start recommendations
        """
        # Define mood embeddings or features
        mood_features = {
            'happy': [1.0, 0.8, 0.6],
            'motivated': [0.9, 1.0, 0.7],
            'relaxed': [0.5, 0.3, 1.0],
            'focused': [0.8, 0.9, 0.4],
            'energetic': [1.0, 0.9, 0.8]
        }
        
        return np.array(mood_features.get(mood.lower(), [0.5, 0.5, 0.5]))