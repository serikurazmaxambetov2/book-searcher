from aiohttp import ClientSession

from ..config import BACKEND_URL


class Api:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def search(self, text: str, page: int = 1):
        async with ClientSession(self.base_url) as session:
            params = {"text": text, "page": page}
            response = await session.get("/search", params=params)

            return await response.json()


api_service = Api(BACKEND_URL)
