from fastapi import FastAPI

from src.todoitem_router import router

app = FastAPI()

app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", reload=True)
