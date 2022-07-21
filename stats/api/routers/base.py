from datetime import datetime

from fastapi import APIRouter

from stats.api.services import base

router = APIRouter()


@router.get('/info/{nickname}')
async def get_info(nickname: str,
                   date_start: datetime = None,
                   date_end: datetime = None):
    return await base.get_info(nickname, date_start, date_end)
