from fastapi import Depends, FastAPI

app = FastAPI()


def my_dependency(query_string: str = None):
    ... # Executa algo antes da requisição
    return  query_string  # Retorna o valor para continuar requisição


@app.get("/")
async def my_route(dependency: str = Depends(my_dependency)):
    return {"message": dependency}