import requests
import json
import os
import time
import git
from git import Repo
from timeit import default_timer as timer

def get_user():
    name = input('''The name of the repo-user/owner:\n
Basically lookin for https://github.com/<user>: \n ''' )
    return name

def get_list():
    username = get_user()
    global repo_list
    url = "https://api.github.com/users/{}/repos".format(username)
    url_name = "https://api.github.com/users/{}".format(username)
    payload={}
    headers = {}
    try:
        response_user = requests.request("GET", url_name, headers=headers, data=payload)
        if response_user.status_code == 200:
            response = requests.request("GET", url, headers=headers, data=payload)
            resp_json = response.json()
            for iter in resp_json:
                repo_list.append(iter['clone_url'])
            if wish == 1:
                print(repo_list)
    except Exception as arr:
        print(arr)

def get_clone():
    get_list()
    pwd = os.environ['PWD']
    location = os.path.join(pwd, 'GoldMine')
    print('This will clone all the repos to a new directory \n{}'.format(location))
    try:
        os.makedirs(location)
    except OSError as err:
        print(err)
    
    try:
        for link in range(len(repo_list)):
            components = repo_list[link].split('/')
            locatn = os.path.join(location, components[-1])
            print('Cloning repo {}'.format(components[-1]))
            start = timer()
            Repo.clone_from(repo_list[link], locatn)
            end = timer()
            print('Repo {} cloned in {} seconds'.format(components[-1],(end - start)))
    except Exception as brr:
        print(brr)

repo_list = []
wish = int(input('''############################
What would you like to do?
1)List the repos owned by a user
2)Clone the all public repos owned by a user
############################################\n'''))
if wish == 1:
    get_list()
elif wish == 2:
    get_clone()
else:
    print('You Dimwit!!')
