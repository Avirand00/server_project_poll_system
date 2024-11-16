from typing import Optional
import httpx
from api.internalApi.userService.model.user import User
from config.config import Config

config = Config()


async def get_user_by_id(user_id: int) -> Optional[User]:
    url = f"{config.USER_SERVICE_BASE_URL}/user/{user_id}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            user = response.json()
            return User(**user)

        except httpx.HTTPStatusError as exception:
            print(f"Error in getting user details: {exception.response}")




