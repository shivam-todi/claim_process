from pydantic import BaseModel, conint

class ClaimDetails(BaseModel):
    plan_number: str
    subscriber: int
    provider_npi: conint(ge=0, le=9223372036854775807)
    service_date: str
    submitted_procedure: str
    quadrant: str
    provider_fees: int
    allowed_fees: int
    member_coinsurance: int
    member_copay: int
    
    class Config:
        orm_mode = True
