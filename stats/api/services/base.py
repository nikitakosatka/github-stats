from datetime import datetime, timedelta
from math import ceil

import requests

from stats.api.utils import GITHUB_TOKEN, DAYS_IN_YEAR
from stats.api.schemas import UserInfo


async def get_base_info(nickname: str) -> UserInfo:
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
        print(response)

        return UserInfo(login=nickname,
                        name=response['name'],
                        stars=stars,
                        pull_requests=response['pullRequests']['totalCount'],
                        issues=response['issues']['totalCount'],
                        contributed_to=response['repositoriesContributedTo'][
                            'totalCount'],
                        created_at=response['createdAt'])


async def count_user_commits(nickname: str, date_start: datetime,
                             date_end: datetime):
    years_count = ceil((date_end - date_start).days / DAYS_IN_YEAR)
    cur_date_end = date_start

    commits = 0

    for year in range(years_count):
        cur_date_start = date_start + timedelta(DAYS_IN_YEAR * year)
        cur_date_end = min(date_end, cur_date_end + timedelta(DAYS_IN_YEAR))

        response = await get_api_response(nickname, cur_date_start,
                                          cur_date_end)

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


async def get_api_response(nickname: str,
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
        date_start = datetime.now() - timedelta(DAYS_IN_YEAR)

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


async def get_info(nickname: str, date_start: datetime, date_end: datetime):
    user_info = await get_base_info(nickname)

    if not date_end:
        date_end = datetime.now().replace(tzinfo=None)

    if not date_start:
        date_start = user_info.created_at.replace(tzinfo=None)

    user_info.commits = await count_user_commits(nickname, date_start, date_end)

    return user_info
