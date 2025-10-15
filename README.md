# Digital-Twin-AI-ChatBot
[![Static Badge](https://img.shields.io/badge/Trello-Kanban-blue?style=flat&logo=trello&logoSize=auto)](https://trello.com/invite/b/68df8720f3a0b9358e3185e0/ATTI3cda1388218acd2b02eaf76dfd1ed374FD152D68/digital-twin)

## Tools
- [uv](https://github.com/astral-sh/uv) for dependency management
    - See [uv.md](docs/uv.md) for a brief guide
- [Trello](https://trello.com/invite/b/68df8720f3a0b9358e3185e0/ATTIf4dc42546f45cbc8140669f8207642abE25BF06A/digital-twin) for project kanban

## How to run
You need to have Docker Desktop up and runningon your machine and a .env file, there is an exmample on branch, then you need to type on your terminal 
```bash
docker compose up --watch
```

The watch flag makes so ... 

## How to close docker
Just run on your terminal
```bash
docker compose down 
```
This is Kill your DataBase, it will only chage when we create Volumes

## How to run the tests
```bash
uv run pytest
```
It will also be run whenever the main branch is updated. The result will appear in GitHub Actions.
