import uvicorn
from db_connection import get_user_scores_with_category_names
from fastapi import FastAPI, Request

app = FastAPI()


@app.post("/analizar-respuestas")
async def analizar_respuestas_usuario(request: Request):
    """Analyzes positive responses by area for a given user ID."""
    data = await request.json()
    user_id = data.get("userId")

    if not user_id:
        return {"error": "Falta userId"}

    try:
        puntajes = get_user_scores_with_category_names(user_id)
        return {"puntajes": puntajes}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5055)
