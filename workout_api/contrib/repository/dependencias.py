from typing import Annotated

from fastapi import Depends
from workout_api.configs.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession


DatabaseDependency = Annotated[AsyncSession, Depends(get_session)]