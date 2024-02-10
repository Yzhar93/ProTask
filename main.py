from fastapi import FastAPI, Form
from fastapi import HTTPException
from pydantic import BaseModel

tasks = {}
users = {}
app = FastAPI()


class Task(BaseModel):
    id: int
    name: str
    description: str


class User(BaseModel):
    id: int
    name: str


@app.get('/')
async def root():
    return {'project': 'fastapi', 'data': 999}


@app.post('/{user_id}/tasks/', tags=['tasks'])
async def add_task(user_id: int, task: Task):
    try:
        if user_id in tasks:
            tasks[user_id].append(task)
            status = 200
        else:
            tasks[user_id] = []
            tasks[user_id].append(task)
            status = 201
    except:
        status = 404

    return {user_id: status}


@app.post('/users/', tags=['users'])
async def add_user(id: int = Form(...), name: str = Form(...)):
    try:
        if id not in users:
            user = User(id=id, name=name)
            users[id] = user
            return {'id': id, 'name': name}
        else:
            return {'error': 'not such user'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get('/users/{id}')
async def get_user(id: int):
    if id in users:
        return {200: users[id]}
    else:
        return {404: 'user  does not exists'}


@app.get('/users/')
async def get_user():
    return users
