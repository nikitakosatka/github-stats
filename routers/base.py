from datetime import datetime

import grpc
from google.protobuf.timestamp_pb2 import Timestamp
from fastapi import APIRouter

from github_fetcher.api.services.github_fetcher_pb2 import GithubFetcherRequest
from github_fetcher.api.services.github_fetcher_pb2_grpc import \
    GithubFetcherStub
from github_fetcher.api.schemas import UserInfo

router = APIRouter()

github_fetcher_channel = grpc.insecure_channel('localhost:50051')

github_fetcher_client = GithubFetcherStub(github_fetcher_channel)


@router.get('/info/{nickname}')
def get_info(nickname: str,
             date_start: datetime = None,
             date_end: datetime = None):
    timestamp_start = Timestamp()
    timestamp_end = Timestamp()

    if date_start:
        timestamp_start.FromDatetime(date_start)

    if date_end:
        timestamp_end.FromDatetime(date_end)
    else:
        timestamp_end.FromDatetime(datetime.now())

    request = GithubFetcherRequest(login=nickname,
                                   date_start=timestamp_start,
                                   date_end=timestamp_end)

    response = github_fetcher_client.get_info(request)
    created_at = datetime.fromtimestamp(
        response.created_at.seconds + response.created_at.nanos / 1e9)

    return UserInfo(name=response.name,
                    login=response.login,
                    stars=response.stars,
                    commits=response.commits,
                    pull_requests=response.pull_requests,
                    issues=response.issues,
                    contributed_to=response.contributed_to,
                    created_at=created_at)
