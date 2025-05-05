from typing import Any, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.db_connection import get_user_from_db


class ActionHandleGreetings(Action):
    """Action to handle greetings."""

    def name(self) -> str:
        """Return the name of the action."""
        return "action_handle_greetings"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Return a list of greetings."""
        in_test = tracker.get_slot("in_test")
        if in_test:
            dispatcher.utter_message(
                text="Estamos en medio del test vocacional. "
                "Terminémoslo antes de continuar."
            )
            return []

        user_name = get_user_from_db()
        current_count = tracker.get_slot("greetings_count") or 0
        new_count = current_count + 1

        if user_name:
            if new_count > 1:
                dispatcher.utter_message(
                    text=f"Hola de nuevo {user_name}, "
                    f"¿Estás preparado para realizar tu evaluación vocacional?",
                )
            else:
                dispatcher.utter_message(
                    text=f"Hola {user_name}, "
                    f"¿Estás preparado para realizar tu evaluación vocacional?",
                )
        else:
            if new_count > 1:
                dispatcher.utter_message(
                    text="Hola de nuevo, "
                    "¿Estás preparado para realizar tu evaluación vocacional?",
                )
            else:
                dispatcher.utter_message(
                    text="Hola, "
                    "¿Estás preparado para realizar tu evaluación vocacional?",
                )

        return [SlotSet("greetings_count", new_count)]


class ActionCheckUserReady(Action):
    """Action to check the user is ready."""

    def name(self) -> str:
        """Return the name of the action."""
        return "action_check_user_ready"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Check if the user is ready and send an appropriate message."""
        user_ready = tracker.get_slot("user_ready")

        if user_ready == "true":
            dispatcher.utter_message(response="utter_user_ready")
            return [SlotSet("in_test", True)]
        elif user_ready == "false":
            dispatcher.utter_message(response="utter_user_not_ready")

        return []


class ActionCheckUserStatus(Action):
    """Action to check the user status."""

    def name(self) -> str:
        """Return the name of the action."""
        return "action_check_user_status"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Check the user status and send an appropriate message."""
        user_status = tracker.get_slot("user_status")

        if user_status == "true":
            dispatcher.utter_message(response="utter_user_status_ok")
        elif user_status == "false":
            dispatcher.utter_message(response="utter_user_status_not_yet")

        return []


class ActionEndTest(Action):
    """Action to mark the end of the vocational test."""

    def name(self) -> str:
        """Return the name of the action."""
        return "action_end_test"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Run the action to finalize the test."""
        dispatcher.utter_message(text="¡Has completado el test vocacional!")
        return [SlotSet("in_test", False)]
