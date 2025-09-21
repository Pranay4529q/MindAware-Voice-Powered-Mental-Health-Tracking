from pydantic import BaseModel
from typing import Dict, List, Any, Optional

class PredictionResponse(BaseModel):
    overall_prediction: Dict[str, Any]
    average_probabilities: Dict[str, float]
    segment_predictions: List[Dict[str, Any]]
    total_segments: int
    record_id: Optional[str] = None

class HistoryResponse(BaseModel):
    id: str
    timestamp: str
    overall_class: int
    class_label: str
    confidence: float
    probabilities: Dict[str, float]

class RecordResponse(BaseModel):
    id: str
    timestamp: str
    overall_class: int
    class_label: str
    confidence: float
    probabilities: Dict[str, float]