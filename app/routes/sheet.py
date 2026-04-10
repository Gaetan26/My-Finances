
from fastapi import APIRouter, Response, status
from models.pydantic import sheet as sheet_models
from services import sheet as sheet_services
from utils.logger import logger

router = APIRouter()

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
