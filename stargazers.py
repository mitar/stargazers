#!/usr/bin/env python

import requests

GITHUB_ACCESS_TOKEN = None
REPOSITORIES = ()

import local_settings

GITHUB_ACCESS_TOKEN = getattr(local_settings, 'GITHUB_ACCESS_TOKEN', None)
REPOSITORIES += getattr(local_settings, 'REPOSITORIES', ())

if not GITHUB_ACCESS_TOKEN:
    raise Exception("GitHub access token is not configured.")

PAGE_SIZE = 100

def github_api(url, args=None):
    if args is None:
        args = {}
    args.update({
        'per_page': PAGE_SIZE,
        'access_token': GITHUB_ACCESS_TOKEN,
    })

    data = []

    next_page = url
    while next_page:
        response = requests.get(url=next_page, params=args)
        d = response.json()

        if not isinstance(d, list):
            if d.get('message', None) == 'Git Repository is empty.':
                return data
            raise Exception(d)

        data.extend(d)

        next_page = response.links.get('next', {}).get('url', None)
        args = {} # To not have duplicate params in the URL

    return data

def get_contact(stargazer):
    repos = github_api(stargazer['repos_url'])
    for repo in repos:
        commits = github_api(repo['commits_url'][:-6])
        for commit in commits:
            if commit['author'] and commit['author']['id'] == stargazer['id']:
                return '%s %s' % (commit['commit']['author']['email'], commit['commit']['author']['name'])
            if commit['committer'] and commit['committer']['id'] == stargazer['id']:
                return '%s %s' % (commit['committer']['author']['email'], commit['committer']['author']['name'])

for github_repository in REPOSITORIES:
    stargazers = github_api('https://api.github.com/repos/%s/stargazers' % github_repository)

    for stargazer in stargazers:
        contact = get_contact(stargazer)
        if contact and contact.find('users.noreply.github.com') == -1:
            print contact.encode('utf-8')
