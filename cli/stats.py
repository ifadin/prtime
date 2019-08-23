from datetime import datetime, timedelta
from typing import List, Tuple

import click
from github import Github
from pandas import DataFrame


def get_analysis(gh: Github, repos: List[str], last_days: int) -> Tuple[DataFrame, DataFrame]:
    data = get_pr_data(gh, repos, last_days)
    time = data.groupby('repo')['Time']
    stats = DataFrame({
        'PRs': time.count(),
        'mean': time.mean(),
        'std': time.std(),
        '50%': time.quantile(q=.5),
        '95%': time.quantile(q=.95),
        '99%': time.quantile(q=.99)
    })

    return stats, data


def get_pr_data(gh: Github, repos: List[str], last_days: int) -> DataFrame:
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
