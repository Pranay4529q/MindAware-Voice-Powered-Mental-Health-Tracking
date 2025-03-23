# from flask import Blueprint, request, jsonify, current_app
# from flask_jwt_extended import jwt_required, get_jwt_identity
# import torch

# from models.audio_record import AudioRecord
# from utils.audio_processing import process_audio_file

# # Create blueprint
# audio_bp = Blueprint('audio', __name__)

# @audio_bp.route('/predict', methods=['POST'])
# @jwt_required()
# def predict():
#     """Process an audio file and return predictions."""
#     # Get current user
#     username = get_jwt_identity()
    
#     # Check if an audio file was uploaded
#     if 'audio' not in request.files:
#         return jsonify({'error': 'No audio file provided'}), 400
    
#     # Get audio file
#     audio_file = request.files['audio']
    
#     # Get model and device
#     model = current_app.model
#     device = current_app.device
#     config = current_app.config
    
#     try:
#         # Process audio file
#         result = process_audio_file(audio_file, model, device, config)
        
#         if 'error' in result:
#             return jsonify(result), 500
        
#         # Save the results to the database
#         overall_prediction = result['overall_prediction']
#         avg_probabilities = result['average_probabilities']
        
#         # Create record
#         record = AudioRecord.create(
#             username=username,
#             overall_class=overall_prediction['predicted_class'],
#             confidence=overall_prediction['confidence'],
#             probabilities=avg_probabilities
#         )
        
#         # Add record ID to result
#         if record:
#             result['record_id'] = str(record['_id'])
        
#         return jsonify(result), 200
    
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @audio_bp.route('/history', methods=['GET'])
# @jwt_required()
# def get_history():
#     """Get the current user's audio analysis history."""
#     # Get current user
#     username = get_jwt_identity()
    
#     # Get history
#     records = AudioRecord.get_user_history(username)
    
#     # Format records
#     class_labels = current_app.config['CLASS_LABELS']
#     history = []
    
#     for record in records:
#         history.append({
#             'id': str(record['_id']),
#             'timestamp': record['timestamp'].isoformat(),
#             'overall_class': record['overall_class'],
#             'class_label': class_labels[record['overall_class']],
#             'confidence': record['confidence'],
#             'probabilities': record['probabilities']
#         })
    
#     return jsonify(history), 200

# @audio_bp.route('/history/<record_id>', methods=['GET'])
# @jwt_required()
# def get_record(record_id):
#     """Get a specific audio analysis record."""
#     # Get current user
#     username = get_jwt_identity()
    
#     # Get record
#     record = AudioRecord.get_by_id(record_id, username)
    
#     if not record:
#         return jsonify({'error': 'Record not found'}), 404
    
#     # Format record
#     class_labels = current_app.config['CLASS_LABELS']
#     formatted_record = {
#         'id': str(record['_id']),
#         'timestamp': record['timestamp'].isoformat(),
#         'overall_class': record['overall_class'],
#         'class_label': class_labels[record['overall_class']],
#         'confidence': record['confidence'],
#         'probabilities': record['probabilities']
#     }
    
#     return jsonify(formatted_record), 200
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
import torch

from models.audio_record import AudioRecord
from utils.audio_processing import process_audio_file

# Create blueprint
audio_bp = Blueprint('audio', __name__)

@audio_bp.route('/predict', methods=['POST'])
@jwt_required()
def predict():
    """Process an audio file and return predictions."""
    # Get current user
    username = get_jwt_identity()
    
    # Check if an audio file was uploaded
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    # Get audio file
    audio_file = request.files['audio']
    
    # Get model and device 
    model = current_app.model if hasattr(current_app, 'model') else None
    device = current_app.device if hasattr(current_app, 'device') else None
    
    if model is None or device is None:
        return jsonify({'error': 'Model or device not initialized'}), 500
    
    try:
        # Process audio file
        result = process_audio_file(audio_file, model, device, current_app.config)
        
        if 'error' in result:
            return jsonify(result), 500
        
        # Save the results to the database
        overall_prediction = result['overall_prediction']
        avg_probabilities = result['average_probabilities']
        
        # Create record
        record = AudioRecord.create(
            username=username,
            overall_class=overall_prediction['predicted_class'],
            confidence=overall_prediction['confidence'],
            probabilities=avg_probabilities
        )
        
        # Add record ID to result
        if record:
            result['record_id'] = str(record['_id'])
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@audio_bp.route('/history', methods=['GET'])
@jwt_required()
def get_history():
    """Get the current user's audio analysis history."""
    # Get current user
    username = get_jwt_identity()
    
    # Get history
    records = AudioRecord.get_user_history(username)
    
    # Format records
    class_labels = current_app.config['CLASS_LABELS']
    history = []
    
    for record in records:
        history.append({
            'id': str(record['_id']),
            'timestamp': record['timestamp'].isoformat(),
            'overall_class': record['overall_class'],
            'class_label': class_labels[record['overall_class']],
            'confidence': record['confidence'],
            'probabilities': record['probabilities']
        })
    
    return jsonify(history), 200

@audio_bp.route('/history/<record_id>', methods=['GET'])
@jwt_required()
def get_record(record_id):
    """Get a specific audio analysis record."""
    # Get current user
    username = get_jwt_identity()
    
    # Get record
    record = AudioRecord.get_by_id(record_id, username)
    
    if not record:
        return jsonify({'error': 'Record not found'}), 404
    
    # Format record
    class_labels = current_app.config['CLASS_LABELS']
    formatted_record = {
        'id': str(record['_id']),
        'timestamp': record['timestamp'].isoformat(),
        'overall_class': record['overall_class'],
        'class_label': class_labels[record['overall_class']],
        'confidence': record['confidence'],
        'probabilities': record['probabilities']
    }
    
    return jsonify(formatted_record), 200