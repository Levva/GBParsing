import requests
import json

git_user = 'sunshineo'
# uncomment for manual input other users
# git_user = input('Need user-name: ')
git_link = 'https://api.github.com/users/' + git_user + '/repos'

response = requests.get(git_link)

if response.ok:
    user_repos = json.loads(response.text)
    print(f'Список репозиториев пользователя {git_user}:')
    for i in range(len(user_repos)):
        print(f"{i+1}. {user_repos[i]['name']}")
else:
    print(f'A user named {git_user} was not found.')
