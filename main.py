import uvicorn
import uuid
import os
from fastapi import FastAPI, HTTPException
from typing import List
from sqlalchemy import desc, func, distinct
from fastapi_sqlalchemy import DBSessionMiddleware, db
from models import ClaimDetails as ModelClaimDetails
from schema import ClaimDetails as SchemaClaimDetails
from dotenv import load_dotenv


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])

@app.post("/claim-details/")
async def create_claim_details(claim_details: List[SchemaClaimDetails]):

    claim_uuid = uuid.uuid1()
    for claim in claim_details:
        if len(str(claim.provider_npi)) != 10:
            raise HTTPException(status_code=400, detail=str("Provider NPI must be 10 characters long"))
        
        if claim.submitted_procedure[0] != 'D':
            raise HTTPException(status_code=400, detail=str("Submitted Procedure must start with D"))

        claim_detail = ModelClaimDetails(
            plan_number=claim.plan_number,
            subscriber=claim.subscriber, provider_npi=claim.provider_npi,
            service_date=claim.service_date, submitted_procedure=claim.submitted_procedure,
            quadrant=claim.quadrant, provider_fees=claim.provider_fees,
            allowed_fees=claim.allowed_fees, member_coinsurance=claim.member_coinsurance,
            member_copay=claim.member_copay, claim_id = claim_uuid,
            net_fees=claim.provider_fees + claim.member_coinsurance + claim.member_copay - claim.allowed_fees
        )
        db.session.add(claim_detail)
    db.session.commit()
    return

@app.get("/provider-npi/top-10/")
async def get_top_10_npi():
    top_providers = (
        db.session.query(distinct(ModelClaimDetails.provider_npi),
            func.sum(ModelClaimDetails.net_fees).label("net_fees_sum")).
            group_by(ModelClaimDetails.provider_npi).
            order_by(desc(func.sum(ModelClaimDetails.net_fees))).
            limit(10).all()
        )

    result = [{"provider_npi": provider_npi, "net_fees_sum": net_fees_sum} for provider_npi, net_fees_sum in top_providers]
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
