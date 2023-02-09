from fastapi import HTTPException, APIRouter, Request
import Viirtue
import secrets
import config

router = APIRouter()


@router.post("/")
async def listen_Calls(request: Request):
    try:
        call = await request.json()
    except:
        raise HTTPException(status_code=400, detail="Invalid request")

    callData = call[0]

    if 'term_sub' in callData and callData['term_sub'] == secrets.buffer_queue:
        number = callData['orig_id']

        if len(number) > 10:
            number = number[len(number) - 10::]

        try:
            if Viirtue.RequestProcessor.conditionsAreRight(number):
                Viirtue.RequestProcessor.transferCall(config.globalToken, number, callData['orig_callid'])
        except:
            pass
