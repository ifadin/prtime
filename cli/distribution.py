from datetime import datetime, timedelta
from typing import List

import click
from github import Github
from pandas import DataFrame


def get_time_analysis(gh: Github, repos: List[str], last_days: int, verbose: bool) -> DataFrame:
    df = get_time_data(gh, repos, last_days)
    if verbose:
        click.echo(df.sort_values('Time', ascending=False))

    count = df.groupby('repo')['Time'].count()
    mean = df.groupby('repo')['Time'].mean()
    sem = df.groupby('repo')['Time'].sem()

    return DataFrame({'PRs': count, 'mean': mean, 'sem': sem, 'window_left': mean - sem, 'window_right': mean + sem})


def get_time_data(gh: Github, repos: List[str], last_days: int) -> DataFrame:
    items = []
    for repo in repos:
        pulls = gh.get_repo(repo).get_pulls(state='closed')
        if not pulls:
            click.echo(f'Could not find any matching pull requests in \'{repo}\'')
        for pr in pulls:
            if ((pr.created_at >= datetime.today() - timedelta(days=last_days)) if last_days else True) and pr.merged:
                pr_time = (pr.merged_at - pr.created_at).total_seconds() / 3600
                items.append((repo, pr.title, pr_time))

    return DataFrame(items, columns=['repo', 'PR', 'Time'])
