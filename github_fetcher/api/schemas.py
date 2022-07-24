from datetime import datetime

from pydantic import BaseModel


class UserInfo(BaseModel):
    name: str | None = None
    login: str
    stars: int = 0
    commits: int = 0
    pull_requests: int = 0
    issues: int = 0
    contributed_to: int = 0
    created_at: datetime
