from rasa_sdk import Action

from actions.db_connection import fetch_questions


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
