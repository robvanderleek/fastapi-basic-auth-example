import secrets
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic
from starlette import status
from starlette.requests import Request
from starlette.staticfiles import StaticFiles


async def verify_credentials(request: Request):
    credentials = await security(request)
    correct_username = secrets.compare_digest(credentials.username, "myuser")
    correct_password = secrets.compare_digest(credentials.password, "mypassword")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )


class AuthStaticFiles(StaticFiles):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    async def __call__(self, scope, receive, send) -> None:
        assert scope["type"] == "http"
        request = Request(scope, receive)
        await verify_credentials(request)
        await super().__call__(scope, receive, send)


security = HTTPBasic()

app = FastAPI(dependencies=[Depends(security)])
app_api = FastAPI()
app.mount('/api', app_api, name='api')
app.mount('/', AuthStaticFiles(directory=Path(__file__).resolve().parent.joinpath('static'), html=True),
          name='static')


@app_api.get("/hello", status_code=200)
async def webhook_succeed(_=Depends(verify_credentials)):
    return "world"


if __name__ == "__main__":
    uvicorn.run('main:app', host='0.0.0.0', port=8080)
