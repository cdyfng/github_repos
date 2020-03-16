# -*- coding:utf-8 -*-
import json
import time
import requests
import numpy as np
import pandas as pd

import requests
from requests.auth import HTTPBasicAuth

import sys
reload(sys)
sys.setdefaultencoding('utf8')
credentials = json.loads(open('credentials.json').read())
authentication = HTTPBasicAuth(
    credentials['username'], credentials['password'])


def get_repos(user):
    data = requests.get('https://api.github.com/users/' +
                        user, auth=authentication)
    #data = requests.get('https://api.github.com/users/' + credentials['username'], auth = authentication)
    data = data.json()

    print("data:", data)
    print("Information about user {}:\n".format(user))
    print("Name: {}".format(data['name']))
    print("Email: {}".format(data['email']))
    print("Location: {}".format(data['location']))
    print("Public repos: {}".format(data['public_repos']))
    print("Public gists: {}".format(data['public_gists']))
    print("About: {}\n".format(data['bio']))

    print("Collecting repositories information")
    url = data['repos_url']
    page_no = 1
    repos_data = []
    # response = requests.get(url, auth = authentication)
    # #response = requests.get(url)
    # response = response.json()
    # repos_data = repos_data + response
    time.sleep(5)
    while (True):
        response = requests.get(url, auth=authentication)
        #response = requests.get(url)
        response = response.json()
        repos_data = repos_data + response
        repos_fetched = len(response)
        print("Total repositories fetched: {}".format(repos_fetched))
        if (repos_fetched == 30):
            page_no = page_no + 1
            url = data['repos_url'] + '?page=' + str(page_no)
        else:
            break
        time.sleep(5)

    repos_information = []
    for i, repo in enumerate(repos_data):
        data = []
        data.append(repo['id'])
        data.append(repo['name'])
        data.append(repo['description'])
        data.append(repo['created_at'])
        data.append(repo['updated_at'])
        data.append(repo['owner']['login'])
        data.append(repo['license']['name']
                    if repo['license'] != None else None)
        data.append(repo['has_wiki'])
        data.append(repo['forks_count'])
        data.append(repo['open_issues_count'])
        data.append(repo['stargazers_count'])
        data.append(repo['watchers_count'])
        data.append(repo['url'])
        data.append(repo['commits_url'].split("{")[0])
        data.append(repo['url'] + '/languages')
        repos_information.append(data)
    return repos_information


f = open("users.csv")
line = f.readline()


while line:
    #all_repos = []
    try:
        user = line.strip(' @').split(' ')
        print(user[0])
        r = get_repos(user[0])

        print('r:', len(r))
        # all_repos.append(r)
        repos_df = pd.DataFrame(r, columns=['Id', 'Name', 'Description', 'Created on', 'Updated on',
                                            'Owner', 'License', 'Includes wiki', 'Forks count',
                                            'Issues count', 'Stars count', 'Watchers count',
                                                          'Repo URL', 'Commits URL', 'Languages URL'])
        repos_df.to_csv('repos_info.csv', mode='a', index=False, header=False)
        # print(line, end = '')
        line = f.readline()
    except:
        print("Connection refused by the server..")
        print("Let me sleep for 5 seconds")
        print("ZZzzzz...")
        time.sleep(60)
        print("Was a nice sleep, now let me continue...")
        line = f.readline()
        continue


f.close()

print("Data collection complete")
