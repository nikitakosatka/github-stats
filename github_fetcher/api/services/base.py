from concurrent import futures
from datetime import datetime

import grpc
import requests
from dateutil.relativedelta import relativedelta
from google.protobuf.timestamp_pb2 import Timestamp

from github_fetcher.api.utils import GITHUB_TOKEN
from github_fetcher.api.schemas import UserInfo
from github_fetcher.api.services.github_fetcher_pb2 import (
    GithubFetcherResponse)
from github_fetcher.api.services import github_fetcher_pb2_grpc


class GithubService(github_fetcher_pb2_grpc.GithubFetcherServicer):
    def get_info(self, request, context):
        date_start = None

        if request.date_start.seconds != 0:
            date_start = datetime.fromtimestamp(
                request.date_start.seconds + request.date_start.nanos / 1e9)

        date_end = datetime.fromtimestamp(
            request.date_end.seconds + request.date_end.nanos / 1e9)
        response = get_info_fetcher(request.login, date_start, date_end)

        created_at = Timestamp()
        created_at.FromDatetime(response.created_at)

        return GithubFetcherResponse(name=response.name,
                                     login=response.login,
                                     stars=response.stars,
                                     commits=response.commits,
                                     pull_requests=response.pull_requests,
                                     issues=response.issues,
                                     contributed_to=response.contributed_to,
                                     created_at=created_at)


def get_base_info(nickname: str) -> UserInfo:
    query = """
            query userInfo($login: String!) {
            user(login: $login) {
              name
              login
              createdAt
              repositoriesContributedTo(
                first: 10
                contributionTypes: [COMMIT, ISSUE, PULL_REQUEST, REPOSITORY]
              ) {
                totalCount
              }
              pullRequests(first: 1) {
                totalCount
              }
              issues {
                totalCount
              }
              followers {
                totalCount
              }
              repositories(
                first: 100
                ownerAffiliations: OWNER
                orderBy: {direction: DESC, field: STARGAZERS}
              ) {
                totalCount
                nodes {
                  stargazers {
                    totalCount
                  }
                }
              }
            }
            rateLimit {
              limit
              cost
              remaining
              resetAt
            }
          }
        """
    response = requests.post('https://api.github.com/graphql',
                             json={
                                 'query': query,
                                 'variables': {
                                     'login': nickname
                                 }
                             },
                             headers={"Authorization": GITHUB_TOKEN}).json()[
        'data']['user']

    if response:
        stars = sum(repo['stargazers']['totalCount'] for repo in
                    response['repositories']['nodes'])

        return UserInfo(login=nickname,
                        name=response['name'],
                        stars=stars,
                        pull_requests=response['pullRequests']['totalCount'],
                        issues=response['issues']['totalCount'],
                        contributed_to=response['repositoriesContributedTo'][
                            'totalCount'],
                        created_at=response['createdAt'])


def count_user_commits(nickname: str, date_start: datetime,
                       date_end: datetime):
    years_count = relativedelta(date_end, date_start).years + 1
    cur_date_end = date_start

    commits = 0

    for year in range(0, years_count):
        cur_date_start = date_start + relativedelta(years=year)
        cur_date_end = min(date_end, cur_date_end + relativedelta(years=1))

        response = get_api_response(nickname, cur_date_start, cur_date_end)

        total_commit_contributions = \
            response['data']['user']['contributionsCollection'][
                'totalCommitContributions']
        restricted_contributions = \
            response['data']['user']['contributionsCollection'][
                'restrictedContributionsCount']

        commits += total_commit_contributions + restricted_contributions

        if cur_date_end == date_end:
            break

    return commits


def get_api_response(nickname: str,
                     date_start: datetime = None,
                     date_end: datetime = None):
    query = """
       query userInfo($login: String!, $from: DateTime, $to: DateTime) {
         user(login: $login) {
           name
           login
           createdAt
           contributionsCollection(from: $from, to: $to) {
             totalCommitContributions
             restrictedContributionsCount
           }
           repositoriesContributedTo(
             first: 10
             contributionTypes: [COMMIT, ISSUE, PULL_REQUEST, REPOSITORY]
           ) {
             totalCount
           }
           pullRequests(first: 1) {
             totalCount
           }
           openIssues: issues(states: OPEN) {
             totalCount
           }
           closedIssues: issues(states: CLOSED) {
             totalCount
           }
           followers {
             totalCount
           }
           repositories(
             first: 100
             ownerAffiliations: OWNER
             orderBy: {direction: DESC, field: STARGAZERS}
           ) {
             totalCount
             nodes {
               stargazers {
                 totalCount
               }
             }
           }
         }
         rateLimit {
           limit
           cost
           remaining
           resetAt
         }
       }
       """

    if not date_start:
        date_start = datetime.now() - relativedelta(years=1)

    if not date_end:
        date_end = datetime.now()

    return requests.post('https://api.github.com/graphql',
                         json={
                             'query': query,
                             'variables': {
                                 'login': nickname,
                                 'from': date_start.isoformat(),
                                 'to': date_end.isoformat()
                             }
                         },
                         headers={"Authorization": GITHUB_TOKEN}).json()


def get_info_fetcher(nickname: str,
                     date_start: datetime,
                     date_end: datetime):
    user_info = get_base_info(nickname)

    if not date_end:
        date_end = datetime.now().replace(tzinfo=None)

    if not date_start:
        date_start = user_info.created_at.replace(tzinfo=None)

    user_info.commits = count_user_commits(nickname, date_start, date_end)

    return user_info


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    github_fetcher_pb2_grpc.add_GithubFetcherServicer_to_server(GithubService(),
                                                                server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
