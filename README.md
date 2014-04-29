stargazers
==========

stargazers fetches contact information for all stargazers of a GitHub repository and
outputs them to the standard output.

Configuration
-------------

You should create a file named `local_settings.py` and define the following variables:

* `GITHUB_ACCESS_TOKEN` -- your [GitHub API access token](https://github.com/settings/applications)
* `REPOSITORIES` -- a list of repositories to fetch contact information for, `'project_name/repository_name'`
