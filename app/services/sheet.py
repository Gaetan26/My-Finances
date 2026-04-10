
from core import gspread
from models.pydantic import sheet as sheet_models
from utils.logger import logger
from utils.others import convert_str_to_int

sheet = gspread.client.open("My Finances").worksheet("Transactions")

async def get_balances() -> dict:
    transactions = await get_transactions()
    balances = dict()

    for currency in sheet_models.Currency:
        balances[currency] = 0

    for transaction in transactions:
        amount = transaction['Amount']
        
        if isinstance(amount, str):
            amount = convert_str_to_int(amount)

        if amount:
            balances[transaction['Currency']] += amount

    return balances

async def get_transactions() -> list:
    try:
        transactions = sheet.get_all_records()
        return transactions
    except Exception as exp:
        logger.error(exp)
        return False

async def add_transaction(transaction: sheet_models.Transaction) -> bool:
    try:
        if transaction.type == sheet_models.Type.Outcoming:
            transaction.amount = - transaction.amount
        transaction_values = list(transaction.model_dump().values())
        sheet.append_row(transaction_values)
        return True
    except Exception as exp:
        logger.error(exp)
        return False
