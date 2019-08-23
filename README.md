# prtime

Analyze your pull requests time


## Install

```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -U -r requirements.txt pip
```

## Usage

```bash
    Usage: prtime [OPTIONS] [REPOS]...
    
    Options:
      -l, --login TEXT         Github login. Mutually exclusive with [auth_token] [required]
      -pw, --password TEXT     Github password. Mutually exclusive with [auth_token] [required]
      -t, --auth-token TEXT    Github authentication token. Mutually exclusive with [login, password] [required]
      -c, --config-file PATH   Path to config file (JSON or YAML)
      -u, --base-url TEXT      Github API endpoint URL
      -o, --organization TEXT  Github organization to search repositories in
      -d, --days INTEGER       Limit stats to last n days
      --export-data PATH       Export path for underlying data
      --export-stats PATH      Export path for statistics
      -v, --verbose            Print dataset info
      --help                   Show this message and exit
```

Example:

```bash
    ./prtime ifadin/prtime
```

Repository name must be in <user|org>/<repo> format or use `-o` suffix:

```bash
    ./prtime -o zalando patroni
```


### Authentication

Script requires a Github API [access token](https://github.com/settings/tokens) or Github login/password.

```bash
    ./prtime -l <gh_login> -pw <gh_password> <repo>
```

```bash
    ./prtime -t <gh_access_token> <repo>
```


### Query window

Query window can be supplied with `-d` (in days):

```bash
    ./prtime -d 30 ifadin/prtime
```


### Multiple repositories

Repository argument supports multiple entries:

```bash
    ./prtime ifadin/prtime denysdovhan/wtfjs
```


### Github enterprise

Github Enterprise API URL can be supplied with `-u`  

```bash
    ./prtime -u <gh_enterprise_url>/api/v3 <repo>
```


### Config file

Config file (YAML/JSON) can be supplied with `-c`:

```bash
    ./prtime -c config.yaml
```

Command line arguments have precedence. Authentication arguments are not taken from config.


### Export

Export (CSV) statistic with `--export-stats` and raw data with `--export-data`:

```bash
    ./prtime --export-stats stats.csv ifadin/prtime
```
