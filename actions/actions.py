import uvicorn
from db_connection import fetch_questions
from fastapi import FastAPI, Request
from rasa_sdk import Action

app = FastAPI()


@app.post("/saludo")
async def saludar_usuario(request: Request):
    """Get the greeting from laravel."""
    data = await request.json()
    nombre = data.get("nombre", "desconocido")
    saludo = f"Hola {nombre}, ¿cómo estás? rasa"
    return {"saludo": saludo}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5055)


class ActionListQuestions(Action):
    """Get all the questions."""

    def name(self):
        """Return the name of the action."""
        return "action_list_questions"

    def run(self, dispatcher, tracker, domain):
        """Get the questions."""
        questions = fetch_questions()
        message = "\n".join([q["description"] for q in questions])
        dispatcher.utter_message(
            text=f"Estas son las preguntas disponibles:\n{message}"
        )
        return []
