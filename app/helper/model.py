from pydantic import BaseModel, Field
from typing import Any, Dict, List

class EvalMatch(BaseModel):
    value: int
    metric: str
    tags: Any


class GrafanaAlert(BaseModel):
    title: str
    ruleId: int
    ruleName: str
    state_: str = Field(..., alias='state ')
    evalMatches: List[EvalMatch]
    orgId: int
    dashboardId: int
    panelId: int
    tags: Dict[str, Any]
    ruleUrl: str
    imageUrl: str
    message: str