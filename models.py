from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, BigInteger

Base = declarative_base()

class ClaimDetails(Base):
    __tablename__ = "claim_details"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    plan_number = Column(String) #assuming it as string
    subscriber = Column(Integer) #assuming it as integer
    provider_npi = Column(BigInteger) #assuming it as big integer
    claim_id = Column(String)
    service_date = Column(String)
    submitted_procedure = Column(String)
    quadrant = Column(String)
    provider_fees = Column(Integer)
    allowed_fees = Column(Integer)
    member_coinsurance = Column(Integer)
    member_copay = Column(Integer)
    net_fees = Column(Integer)
