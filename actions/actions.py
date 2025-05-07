from typing import List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import EventType, SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.db_connection import fetch_questions


class ActionFetchQuestions(Action):
    """Get."""

    def name(self) -> str:
        """Get."""
        return "action_fetch_questions"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        """Get."""
        questions = fetch_questions()

        if not questions:
            dispatcher.utter_message(
                text="No hay preguntas disponibles en la base de datos."
            )
            return []

        tracker.slots["questions_list"] = questions
        first_question = questions[0]
        dispatcher.utter_message(text=first_question)
        return [SlotSet("question_index", 0)]


class ActionNextQuestion(Action):
    """Get."""

    def name(self) -> str:
        """Get."""
        return "action_next_question"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict
    ) -> List[EventType]:
        """Get."""
        current_index = int(tracker.get_slot("question_index") or 0)
        questions = fetch_questions()

        next_index = current_index + 1
        if next_index < len(questions):
            dispatcher.utter_message(text=questions[next_index])
            return [SlotSet("question_index", next_index)]
        else:
            dispatcher.utter_message(text="¡Gracias por completar el test!")
            return [SlotSet("question_index", 0)]


class ActionHandleDenial(Action):
    """Get."""

    def name(self) -> str:
        """Get."""
        return "action_handle_denial"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        """Get."""
        dispatcher.utter_message(
            text='No hay problema. Cuando estés listo, solo escribe "estoy listo".'
        )
        return []
