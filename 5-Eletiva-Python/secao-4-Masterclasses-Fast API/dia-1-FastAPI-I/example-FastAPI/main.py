from fastapi import FastAPI

app = FastAPI(title="Olá, mundo!")


@app.get("/")
def home():
    return {"message": "Hello World"}