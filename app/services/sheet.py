
from core import gspread
from models.pydantic import sheet as sheet_models
from utils.logger import logger

sheet = gspread.client.open("My Finances").worksheet("Transactions")

async def get_transactions() -> list:
    try:
        transactions = sheet.get_all_records()
        return transactions
    except Exception as exp:
        logger.error(exp)
        return False

async def add_transaction(transaction: sheet_models.Transaction) -> bool:
    try:
        transaction_values = list(transaction.model_dump().values())
        sheet.append_row(transaction_values)
        return True
    except Exception as exp:
        logger.error(exp)
        return False
