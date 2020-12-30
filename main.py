from configparser import ConfigParser

import requests
from fastapi import FastAPI

# Environment Variables
config_file = "env.ini"
config = ConfigParser()
config.read(config_file)

secret_key = config.get('secrets', 'key')
GITHUB_TOKEN = config.get('secrets', 'github_token')
owner = config.get('secrets', 'owner')
repository = config.get('secrets', 'repository')

app = FastAPI()


@app.get("/")
def home():
    return {'Hello': 'World'}


@app.post("/do")
def action(event_type: str, secret: str):
    if secret == secret_key:
        headers = {
            'Accept': 'application/vnd.github.everest-preview+json',
            'Authorization': f'token {GITHUB_TOKEN}'
        }

        url = f'https://api.github.com/repos/{owner}/{repository}/dispatches'

        data = '{"event_type":"' + event_type + '"}'

        res = requests.post(url, headers=headers, data=data)

        return {'status': res.status_code}
