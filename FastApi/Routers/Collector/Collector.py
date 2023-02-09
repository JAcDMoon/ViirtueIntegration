from fastapi import Depends, HTTPException, APIRouter
from ...Dependencies import get_current_user
import Salesforce
from .responses import *


router = APIRouter(
    prefix="/collector",
    tags=["collector"],
    dependencies=[Depends(get_current_user)],
)


@router.post("/party")
async def new_Party_Listener(party: Party):
    salesforceDatabase = Salesforce.DataBase()
    party.mobile_phone = Salesforce.DataCollector.findPhone(party.mobile_phone)
    party.home_phone = Salesforce.DataCollector.findPhone(party.home_phone)
    party.phone = Salesforce.DataCollector.findPhone(party.phone)

    if party.mobile_phone or party.home_phone or party.phone:
        salesforceDatabase.partiesTriggerEvent(party)

    raise HTTPException(status_code=200)


@router.post("/intake")
async def new_Intake_Listener(intake: Intake):
    salesforceDatabase = Salesforce.DataBase()
    salesforceDatabase.intakesTriggerEvent(intake)
    raise HTTPException(status_code=200)
