import os
import aiofiles
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from fastapi.responses import JSONResponse

from core.config import get_settings
from dependencies import get_ml_service, get_current_user
from models.audio_record import AudioRecord
from services.ml_service import MLService
from schemas.audio import PredictionResponse, HistoryResponse, RecordResponse

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
async def predict_depression(
    audio: UploadFile = File(...),
    current_user: str = Depends(get_current_user),
    ml_service: MLService = Depends(get_ml_service),
    settings = Depends(get_settings)
):
    """Process an audio file and return depression predictions"""
    
    # Validate file type
    if not audio.filename.lower().endswith(tuple(settings.allowed_extensions)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed: {settings.allowed_extensions}"
        )
    
    # Validate file size
    if audio.size and audio.size > settings.max_file_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Max size: {settings.max_file_size} bytes"
        )
    
    # Create temp directory
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, f"temp_{current_user}_{audio.filename}")
    
    try:
        # Save uploaded file
        async with aiofiles.open(temp_path, 'wb') as f:
            content = await audio.read()
            await f.write(content)
        
        # Process audio and get predictions
        result = await ml_service.predict_audio(temp_path, settings)
        
        # Save results to database
        overall_prediction = result['overall_prediction']
        avg_probabilities = result['average_probabilities']
        
        record = await AudioRecord.create(
            username=current_user,
            overall_class=overall_prediction['predicted_class'],
            confidence=overall_prediction['confidence'],
            probabilities=avg_probabilities
        )
        
        # Add record ID to result
        if record:
            result['record_id'] = str(record['_id'])
        
        return JSONResponse(content=result, status_code=200)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Audio processing failed: {str(e)}"
        )
    
    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)

@router.get("/history", response_model=List[HistoryResponse])
async def get_audio_history(
    current_user: str = Depends(get_current_user),
    settings = Depends(get_settings)
):
    """Get the current user's audio analysis history"""
    
    records = await AudioRecord.get_user_history(current_user)
    
    history = []
    for record in records:
        history.append({
            'id': str(record['_id']),
            'timestamp': record['timestamp'].isoformat(),
            'overall_class': record['overall_class'],
            'class_label': settings.class_labels[record['overall_class']],
            'confidence': record['confidence'],
            'probabilities': record['probabilities']
        })
    
    return history

@router.get("/history/{record_id}", response_model=RecordResponse)
async def get_audio_record(
    record_id: str,
    current_user: str = Depends(get_current_user),
    settings = Depends(get_settings)
):
    """Get a specific audio analysis record"""
    
    record = await AudioRecord.get_by_id(record_id, current_user)
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record not found"
        )
    
    formatted_record = {
        'id': str(record['_id']),
        'timestamp': record['timestamp'].isoformat(),
        'overall_class': record['overall_class'],
        'class_label': settings.class_labels[record['overall_class']],
        'confidence': record['confidence'],
        'probabilities': record['probabilities']
    }
    
    return formatted_record