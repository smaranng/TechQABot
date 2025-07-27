# state.py
from typing import TypedDict, List, Optional, Dict

class AgentState(TypedDict, total=False):
    prompt: str
    docs: List[Dict]
    thresholded_docs: List[Dict]
    sim_scores: List[float]
    answer: str
    general_response: Optional[str]
