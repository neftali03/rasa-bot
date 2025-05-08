from typing import List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import EventType, SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.db_connection import fetch_questions


class ActionStartConversation(Action):
    """Manages user readiness to start the test."""

    def name(self) -> str:
        """Return the name of the action."""
        return "action_start_conversation"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        """Start the test or prompts the user based on input."""
        questions = fetch_questions()
        user_message = tracker.latest_message.get("text", "").lower().strip()

        valid_affirm = [
            "sí estoy listo",
            "si estoy listo",
            "sí, sí estoy listo",
            "si, si estoy listo",
        ]
        valid_deny = ["no, no estoy listo", "no, estoy listo", "no estoy listo"]

        if user_message in valid_affirm:
            dispatcher.utter_message(text="Perfecto, comenzamos.")
            if not questions:
                dispatcher.utter_message(
                    text="No hay preguntas disponibles en este momento."
                )
                return []
            tracker.slots["questions_list"] = questions
            first_question = questions[0]
            dispatcher.utter_message(text=first_question)
            return [SlotSet("question_index", 0), SlotSet("is_test_active", True)]
        elif user_message in valid_deny:
            dispatcher.utter_message(
                text='Esta bien. Cuando estés listo, solo escribe "Sí estoy listo".'
            )
            return [SlotSet("is_test_active", False)]
        else:
            dispatcher.utter_message(
                text="Responde únicamente con: 'Sí estoy listo' o 'No estoy listo'."
            )
            return []


class ActionStartQuestion(Action):
    """Displays the next test question or ends the test."""

    def name(self) -> str:
        """Return the name of the action."""
        return "action_start_question"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict
    ) -> List[EventType]:
        """Show the next question or ends the test."""
        current_index = int(tracker.get_slot("question_index") or 0)
        questions = fetch_questions()

        next_index = current_index + 1
        if next_index < len(questions):
            dispatcher.utter_message(text=questions[next_index])
            return [SlotSet("question_index", next_index)]
        else:
            dispatcher.utter_message(text="¡Gracias por completar el test!")
            dispatcher.utter_message(
                text="¡Estas son las carreras que mejor se adaptán a ti!"
            )
            return [SlotSet("question_index", 0), SlotSet("is_test_active", False)]


class ActionInvalidDuringTest(Action):
    """Rejects invalid input during the test."""

    def name(self) -> str:
        """Return the name of the action."""
        return "action_invalid_during_test"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict
    ) -> List[EventType]:
        """Warns user to answer only with 'Sí' or 'No'."""
        dispatcher.utter_message(
            text="Estás en medio del test. Solo puedes responder con 'Sí' o 'No'."
        )
        current_index = int(tracker.get_slot("question_index") or 0)
        questions = fetch_questions()

        if 0 <= current_index < len(questions):
            dispatcher.utter_message(text=questions[current_index])

        return []
