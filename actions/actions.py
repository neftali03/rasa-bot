from typing import Any

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
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Return a list of greetings."""
        user_name = get_user_from_db()
        current_count = tracker.get_slot("greetings_count") or 0
        new_count = current_count + 1

        if new_count > 1:
            dispatcher.utter_message(response="utter_greetings_extra")
        else:
            if user_name:
                dispatcher.utter_message(
                    response="utter_greetings",
                    **{"user_name": user_name},
                )
            else:
                dispatcher.utter_message(response="utter_greetings")

        return [SlotSet("greetings_count", new_count)]


class ActionCheckUserReady(Action):
    """Action to check the user is ready."""

    def name(self) -> str:
        """Return the name of the action."""
        return "action_check_user_ready"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Check if the user is ready and send an appropriate message."""
        user_ready = tracker.get_slot("user_ready")

        if user_ready == "true":
            dispatcher.utter_message(response="utter_user_ready")
        elif user_ready == "false":
            dispatcher.utter_message(response="utter_user_not_ready")

        return []


class ActionCheckUserStatus(Action):
    """Action to check the user status."""

    def name(self) -> str:
        """Return the name of the action."""
        return "action_check_user_status"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Check the user status and send an appropriate message."""
        user_status = tracker.get_slot("user_status")

        if user_status == "true":
            dispatcher.utter_message(response="utter_user_status_ok")
        elif user_status == "false":
            dispatcher.utter_message(response="utter_user_status_not_yet")

        return []
