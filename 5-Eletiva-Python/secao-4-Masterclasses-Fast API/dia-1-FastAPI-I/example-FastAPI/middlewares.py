from fastapi import FastAPI

app = FastAPI()


@app.middleware("http")
async def my_custom_middleware(request: Request, call_next):
    ... # Executa algo antes da requisição
    response = await call_next(request)  # Executa a requisição
    ... # Executa algo depois da requisição
    return response  # Retorna a resposta da requisição