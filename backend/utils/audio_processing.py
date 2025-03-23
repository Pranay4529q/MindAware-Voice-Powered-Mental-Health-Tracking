import numpy as np
import librosa
import torch
import cv2
import os

def load_audio(file_path, sr=16000):
    """
    Load audio file and return the audio time series
    """
    y, _ = librosa.load(file_path, sr=sr)
    return y

def segment_audio(y, segment_length=1.0, sr=16000):
    """
    Segment audio into fixed-length segments
    """
    # Calculate number of samples per segment
    samples_per_segment = int(segment_length * sr)
    
    # Calculate number of segments
    num_segments = len(y) // samples_per_segment
    
    segments = []
    for i in range(num_segments):
        start = i * samples_per_segment
        end = start + samples_per_segment
        segment = y[start:end]
        segments.append(segment)
    
    return segments

def audio_to_melspectrogram(clip, sr=16000, n_fft=1024, hop_length=256, win_length=1024, n_mels=64, d_shape=64):
    """
    Convert audio segment to mel-spectrogram following the exact process from your code
    """
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

def preprocess_audio(file_path, sr=16000, n_fft=1024, hop_length=256, win_length=1024, n_mels=64, d_shape=64):
    """
    Preprocess audio file for model input, following your specific approach
    """
    # Load audio
    y = load_audio(file_path, sr=sr)
    
    # Segment audio
    segments = segment_audio(y, sr=sr)
    
    # Convert each segment to mel-spectrogram
    mel_specs = []
    for segment in segments:
        mel_spec = audio_to_melspectrogram(
            segment, 
            sr=sr, 
            n_fft=n_fft, 
            hop_length=hop_length, 
            win_length=win_length, 
            n_mels=n_mels, 
            d_shape=d_shape
        )
        mel_specs.append(mel_spec)
    
    # Convert to numpy array
    mel_specs = np.array(mel_specs)
    
    # Prepare for PyTorch model (add channel dimension)
    # Shape: (batch_size, 1, d_shape, d_shape)
    mel_specs = np.expand_dims(mel_specs, axis=1)
    mel_specs = torch.FloatTensor(mel_specs)
    
    return mel_specs

# # def process_audio_file(audio_file, model, device, config):

#     """
#     Process an audio file, run it through the model, and return predictions.
    
#     Args:
#         audio_file: The uploaded audio file
#         model: The PyTorch model
#         device: The device (CPU/GPU)
#         config: Application config
        
#     Returns:
#         dict: Prediction results
#     """
#     try:
#         # Create a temporary directory if it doesn't exist
#         temp_dir = os.path.join(os.getcwd(), 'temp')
#         if not os.path.exists(temp_dir):
#             os.makedirs(temp_dir)
        
#         # Save the uploaded file temporarily
#         temp_path = os.path.join(temp_dir, 'temp_audio.wav')
#         audio_file.save(temp_path)
        
#         # Preprocess the audio
#         mel_specs = preprocess_audio(temp_path)
        
#         # Move to device
#         mel_specs = mel_specs.to(device)
        
#         # Run through model
#         model.eval()
#         with torch.no_grad():
#             outputs = model(mel_specs)
#             probabilities = torch.nn.functional.softmax(outputs, dim=1)
            
#             # Get predictions for each segment
#             _, predictions = torch.max(outputs, 1)
            
#             # Convert to numpy for easier processing
#             predictions = predictions.cpu().numpy()
#             probs = probabilities.cpu().numpy()
            
#         # Calculate overall prediction
#         most_common_class = np.bincount(predictions).argmax()
        
#         # Calculate average probabilities
#         avg_probabilities = probs.mean(axis=0).tolist()
        
#         # Get confidence score
#         confidence = avg_probabilities[most_common_class]
        
#         # Clean up temporary file
#         if os.path.exists(temp_path):
#             os.remove(temp_path)
        
#         # Return results
#         return {
#             'overall_prediction': {
#                 'predicted_class': int(most_common_class),
#                 'confidence': float(confidence)
#             },
#             'average_probabilities': avg_probabilities
#         }
#     except Exception as e:
#         return {'error': f"Audio processing failed: {str(e)}"}
# def process_audio_file(audio_file, model, device, config):
#     try:
#         # Save the uploaded file temporarily
#         temp_dir = os.path.join(os.getcwd(), 'temp')
#         if not os.path.exists(temp_dir):
#             os.makedirs(temp_dir)
        
#         temp_path = os.path.join(temp_dir, 'temp_audio.wav')
#         audio_file.save(temp_path)
        
#         # Preprocess the audio
#         mel_specs = preprocess_audio(temp_path)
        
#         # Move to device
#         mel_specs = mel_specs.to(device)
        
#         # Run through model
#         model.eval()
#         with torch.no_grad():
#             # Your model returns (logits, embedding)
#             outputs, _ = model(mel_specs)  # Unpack the tuple, ignoring the embedding
            
#             # Now apply softmax to the logits
#             probabilities = torch.nn.functional.softmax(outputs, dim=1)
            
#             # Get predictions for each segment
#             _, predictions = torch.max(outputs, 1)
            
#             # Convert to numpy for easier processing
#             predictions = predictions.cpu().numpy()
#             probs = probabilities.cpu().numpy()
        
#         # Calculate overall prediction
#         most_common_class = np.bincount(predictions).argmax()
        
#         # Calculate average probabilities
#         avg_probabilities = probs.mean(axis=0).tolist()
        
#         # Get confidence score
#         confidence = avg_probabilities[most_common_class]
        
#         # Clean up temporary file
#         if os.path.exists(temp_path):
#             os.remove(temp_path)
        
#         # Return results
#         return {
#             'overall_prediction': {
#                 'predicted_class': int(most_common_class),
#                 'confidence': float(confidence)
#             },
#             'average_probabilities': avg_probabilities
#         }
#     except Exception as e:
#         return {'error': f"Audio processing failed: {str(e)}"}
def process_audio_file(audio_file, model, device, config):
    try:
        # Save the uploaded file temporarily
        temp_dir = os.path.join(os.getcwd(), 'temp')
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        
        temp_path = os.path.join(temp_dir, 'temp_audio.wav')
        audio_file.save(temp_path)
        
        # Preprocess the audio
        mel_specs = preprocess_audio(temp_path)
        
        # Move to device
        mel_specs = mel_specs.to(device)
        
        # Run through model
        model.eval()
        with torch.no_grad():
            # Your model returns (logits, embedding)
            outputs, _ = model(mel_specs)  # Unpack the tuple, ignoring the embedding
            
            # Now apply softmax to the logits
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            
            # Get predictions for each segment
            _, predictions = torch.max(outputs, 1)
            
            # Convert to numpy for easier processing
            predictions = predictions.cpu().numpy()
            probs = probabilities.cpu().numpy()
        
        # Calculate overall prediction
        most_common_class = np.bincount(predictions).argmax()
        
        # Calculate average probabilities
        avg_probabilities = probs.mean(axis=0).tolist()
        
        # Get confidence score
        confidence = avg_probabilities[most_common_class]
        
        # Get class labels
        class_labels = config.get('CLASS_LABELS', ['Minimal', 'Moderate', 'Severe'])
        
        # Create segment predictions
        segment_predictions = []
        for i, (pred, prob) in enumerate(zip(predictions, probs)):
            segment_predictions.append({
                'segment': i,
                'predicted_class': int(pred),
                'class_label': class_labels[int(pred)],
                'probabilities': {class_labels[j]: float(p) for j, p in enumerate(prob)}
            })
        
        # Clean up temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        # Return results
        return {
            'overall_prediction': {
                'predicted_class': int(most_common_class),
                'confidence': float(confidence),
                'class_label': class_labels[most_common_class]
            },
            'average_probabilities': {class_labels[i]: float(p) for i, p in enumerate(avg_probabilities)},
            'segment_predictions': segment_predictions
        }
    except Exception as e:
        return {'error': f"Audio processing failed: {str(e)}"}