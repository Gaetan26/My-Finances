
from core import gspread
from models.pydantic import sheet as sheet_models
from utils.logger import logger
from utils.others import convert_str_to_int
from uuid import uuid4
from core.env import FINANCES_RENDER_SERVICE
import httpx

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

async def get_transactions_html(transactions):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            FINANCES_RENDER_SERVICE + '/html',
            json={ 'transactions': transactions },
            timeout=10.0
        )

        if response.status_code != 200:
            return None
        
        return response.content

async def get_transactions_image(transactions):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            FINANCES_RENDER_SERVICE + '/image',
            json={ 'transactions': transactions },
            timeout=10.0
        )

        if response.status_code != 200:
            return None
        
        return response.content

async def get_latests_transactions(number: int) -> list:
    if number <= 0:
        return None

    transactions = await get_transactions()
    latests = []

    if number > len(transactions):
        number = len(transactions)

    for i in range(0, number):
        if isinstance(transactions[i]['Amount'], str):
            transactions[i]['Amount'] = convert_str_to_int(transactions[i]['Amount'])
        latests.append({ 'Id': str(uuid4()), **transactions[i] })
    
    return latests

async def get_transactions() -> list:
    try:
        transactions: list = sheet.get_all_records()
        return list(reversed(transactions))
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
