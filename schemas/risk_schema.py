"""
Risk Schema for Agent 4 (Risk Management Agent)

Purpose:
This schema defines the structured risk management
output used for trade approval and position adjustment.

Why this matters:
- Prevents uncontrolled trading
- Creates institutional-style risk governance
- Enables risk-aware portfolio construction
- Supports gated approval workflows
"""

from pydantic import BaseModel


class RiskOutput(BaseModel):

    # Reference to original event
    event_id: str

    # Final approval decision
    risk_approval: bool

    # Current volatility regime
    risk_regime: str

    # Simulated VIX level
    vix_level: int

    # Position adjustment multiplier
    position_multiplier: float

    # Drawdown control result
    max_drawdown_check: str

    # Turnover control result
    turnover_check: str

    # Risk management explanation
    risk_notes: str