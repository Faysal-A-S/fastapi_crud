from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
def root():
    return {"message":"Hello world"}

@app.get("/users")
def user_list():
    return {"message":"User list"}



if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="127.0.0.1", port=8000, reload=True, log_level="info"
    )