import math
from datetime import datetime, timedelta
from typing import List

import click
from github import Github
from github.Repository import Repository
from pandas import DataFrame


def analyze_repos(gh: Github, repos: List[str], last_days: int, verbose: bool):
    for repo in repos:
        pulls = calculate_pr_time(gh.get_repo(repo), last_days)
        if not pulls.empty:
            if verbose:
                click.echo(pulls.sort_values('Time', ascending=False))
            time_col = pulls.loc[:, 'Time']
            mean = time_col.mean()
            std_err = time_col.std() / math.sqrt(len(time_col))

            click.echo(f'{repo} ({len(time_col)} PRs): '
                       f'mean={mean:.2f}, std_e={std_err:.2f}, window=[{(mean - std_err):.2f}, {(mean + std_err):.2f}]')
        else:
            click.echo(f'Could not find any matching pull requests in \'{repo}\'')


def calculate_pr_time(repo: Repository, last_days: int) -> DataFrame:
    return DataFrame(list(
        {p.title: (p.merged_at - p.created_at).seconds / 3600
         for p in repo.get_pulls(state='closed')
         if ((p.created_at >= datetime.today() - timedelta(days=last_days)) if last_days else True) and p.merged
         }.items()),
        columns=['PR', 'Time']
    )
