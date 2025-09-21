import numpy as np
import librosa
import torch
import cv2
import os
from typing import List

class AudioProcessor:
    """Service for audio processing operations"""
    
    def load_audio(self, file_path: str, sr: int = 16000) -> np.ndarray:
        """Load audio file and return the audio time series"""
        y, _ = librosa.load(file_path, sr=sr)
        return y

    def segment_audio(self, y: np.ndarray, segment_length: float = 1.0, sr: int = 16000) -> List[np.ndarray]:
        """Segment audio into fixed-length segments"""
        samples_per_segment = int(segment_length * sr)
        num_segments = len(y) // samples_per_segment
        
        segments = []
        for i in range(num_segments):
            start = i * samples_per_segment
            end = start + samples_per_segment
            segment = y[start:end]
            segments.append(segment)
        
        return segments

    def audio_to_melspectrogram(
        self, 
        clip: np.ndarray, 
        sr: int = 16000, 
        n_fft: int = 1024, 
        hop_length: int = 256, 
        win_length: int = 1024, 
        n_mels: int = 64, 
        d_shape: int = 64
    ) -> np.ndarray:
        """Convert audio segment to mel-spectrogram"""
        
        # Create mel-spectrogram
        mel_spec = librosa.feature.melspectrogram(
            y=clip, 
            sr=sr, 
            n_mels=n_mels, 
            n_fft=n_fft, 
            hop_length=hop_length, 
            win_length=win_length, 
            window='hann'
        )
        
        # Convert to dB scale
        log_spectrogram = librosa.amplitude_to_db(mel_spec)
        
        # Normalize
        norm = (log_spectrogram - np.min(log_spectrogram)) / (np.max(log_spectrogram) - np.min(log_spectrogram))
        
        # Resize to target shape
        img = cv2.resize(norm, dsize=(d_shape, d_shape), interpolation=cv2.INTER_CUBIC)
        
        return img

    def preprocess_audio(
        self, 
        file_path: str, 
        sr: int = 16000, 
        n_fft: int = 1024, 
        hop_length: int = 256, 
        win_length: int = 1024, 
        n_mels: int = 64, 
        d_shape: int = 64
    ) -> torch.Tensor:
        """Preprocess audio file for model input"""
        
        # Load audio
        y = self.load_audio(file_path, sr=sr)
        
        # Segment audio
        segments = self.segment_audio(y, sr=sr)
        
        # Convert each segment to mel-spectrogram
        mel_specs = []
        for segment in segments:
            mel_spec = self.audio_to_melspectrogram(
                segment, 
                sr=sr, 
                n_fft=n_fft, 
                hop_length=hop_length, 
                win_length=win_length, 
                n_mels=n_mels, 
                d_shape=d_shape
            )
            mel_specs.append(mel_spec)
        
        # Convert to numpy array and add channel dimension
        mel_specs = np.array(mel_specs)
        mel_specs = np.expand_dims(mel_specs, axis=1)
        mel_specs = torch.FloatTensor(mel_specs)
        
        return mel_specs