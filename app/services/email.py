
import httpx
from core.env import MAILGUN_KEY, MAILGUN_BASE_URL
from utils.logger import logger

async def send(from_: str, to: str, subject: str, **kwargs) -> bool:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            MAILGUN_BASE_URL + '/messages',
            auth=httpx.BasicAuth(username='api', password=MAILGUN_KEY),
            files={
                'from': from_,
                'to': to,
                'subject': subject,
                'text': 'TESTING',
                **kwargs
            }
        )

        if response.status_code != 200:
            logger.error(f'email failed for `{to}`, reason: {response.text}')
            return False

    return 200
