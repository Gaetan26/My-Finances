
from fastapi import APIRouter, Response, status, BackgroundTasks
from models.pydantic import sheet as sheet_models
from services import sheet as sheet_services
from services import email as email_services
from utils.logger import logger
from core.env import APP_EMAIL, USER_EMAIL

router = APIRouter()

@router.get("/latests/{number}")
async def get_latests(response: Response, backgound_tasks: BackgroundTasks, number: int, email: bool = False):
    transactions = await sheet_services.get_latests_transactions(number)
    if transactions:

        try:
            image = await sheet_services.get_transactions_image(transactions)

            if email:
                backgound_tasks.add_task(
                    email_services.send, 
                    from_=APP_EMAIL, to=USER_EMAIL, 
                    subject="Here is your financial report",
                    text="You can find your transactions in the report attached to this email",
                    attachment=image
                )
                
                return {
                    'sucess': True
                }
            
            else:
                if image:
                    return Response(content=image, media_type="image/png")
                
        except:
            pass


    logger.error("unable to generate latests transactions report")
    response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return {
        "success": False,
        "error": {
            "content": "were are unable to generate latests transactions report"
        }
    }

@router.get("/balances")
async def get_balances(response: Response):
    balances = await sheet_services.get_balances()

    if balances:
        return {
            "success": True,
            "content": {
                "balances": balances
            }
        }

    return

@router.get('/transactions')
async def get_transactions(response: Response):
    transactions = await sheet_services.get_transactions()

    if isinstance(transactions, list):
        logger.success("all transactions fetched")
        return {
            "success": True,
            "content": {
                "transactions": transactions
            }
        }
    
    logger.error("unable to fetch all transactions")
    response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return {
        "success": False,
        "error": {
            "content": "were are unable to fetch all transactions"
        }
    }


@router.post('/transactions')
async def add_transaction(transaction: sheet_models.Transaction, response: Response):
    transaction = await sheet_services.add_transaction(transaction)

    if transaction:
        logger.success("new transaction created")
        response.status_code = status.HTTP_201_CREATED
        return {
            "success": True,
            "content": {
                "msg": "new transaction created"
            }
        }
    
    logger.error("unable to create new transaction")
    response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return {
        "success": False,
        "content": {
            "error": "were are unable to create new transaction"
        }
    }
