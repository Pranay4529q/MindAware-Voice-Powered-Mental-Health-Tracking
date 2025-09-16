import os
import numpy as np
import torch
import asyncio
from typing import Dict, List, Any
from pathlib import Path

from models.ml_model import load_model
from services.audio_processing import AudioProcessor

class MLService:
    """Service for ML model operations"""
    
    def __init__(self, model_path: str, device: torch.device):
        self.model_path = model_path
        self.device = device
        self.model = None
        self.audio_processor = AudioProcessor()
        
    async def load_model(self) -> None:
        """Load the trained model asynchronously"""
        loop = asyncio.get_event_loop()
        self.model = await loop.run_in_executor(None, load_model, self.model_path, self.device)
    
    async def predict_audio(self, audio_file_path: str, settings) -> Dict[str, Any]:
        """
        Process audio file and return predictions
        """
        if self.model is None:
            raise RuntimeError("Model not loaded")
        
        try:
            # Process audio in thread pool
            loop = asyncio.get_event_loop()
            mel_specs = await loop.run_in_executor(
                None, 
                self.audio_processor.preprocess_audio,
                audio_file_path,
                settings.sample_rate,
                settings.n_fft,
                settings.hop_length,
                settings.win_length,
                settings.n_mels,
                settings.d_shape
            )
            
            # Move to device and predict
            mel_specs = mel_specs.to(self.device)
            
            with torch.no_grad():
                outputs, _ = self.model(mel_specs)
                probabilities = torch.nn.functional.softmax(outputs, dim=1)
                _, predictions = torch.max(outputs, 1)
                
                # Convert to numpy
                predictions = predictions.cpu().numpy()
                probs = probabilities.cpu().numpy()
            
            # Calculate results
            most_common_class = np.bincount(predictions).argmax()
            avg_probabilities = probs.mean(axis=0).tolist()
            confidence = avg_probabilities[most_common_class]
            
            # Create segment predictions
            segment_predictions = []
            for i, (pred, prob) in enumerate(zip(predictions, probs)):
                segment_predictions.append({
                    'segment': i,
                    'predicted_class': int(pred),
                    'class_label': settings.class_labels[int(pred)],
                    'probabilities': {
                        settings.class_labels[j]: float(p) 
                        for j, p in enumerate(prob)
                    }
                })
            
            return {
                'overall_prediction': {
                    'predicted_class': int(most_common_class),
                    'confidence': float(confidence),
                    'class_label': settings.class_labels[most_common_class]
                },
                'average_probabilities': {
                    settings.class_labels[i]: float(p) 
                    for i, p in enumerate(avg_probabilities)
                },
                'segment_predictions': segment_predictions,
                'total_segments': len(predictions)
            }
            
        except Exception as e:
            raise RuntimeError(f"Audio processing failed: {str(e)}")
    
    def is_loaded(self) -> bool:
        """Check if model is loaded"""
        return self.model is not None