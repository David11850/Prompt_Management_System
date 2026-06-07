# prompt management
from fastapi import FastAPI
from route.prompt_api import router
import uvicorn

app=FastAPI()
app.include_router(router)

if __name__=="__main__":
    uvicorn.run("main:app",port=8000,reload=True)