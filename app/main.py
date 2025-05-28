import uvicorn
from fastapi import FastAPI

from app.web.app import create_app

app: FastAPI = create_app()


if __name__ == '__main__':
    uvicorn.run(
        'app.main:app',
        host='0.0.0.0',
        port=8000,
        reload=True,
        env_file='.env'
    )
