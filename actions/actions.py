from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionCheckUserReady(Action):
    def name(self) -> Text:
        return "action_check_user_ready"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_ready = tracker.get_slot("user_ready")

        if user_ready == "true":
            dispatcher.utter_message(response="utter_user_ready")
        elif user_ready == "false":
            dispatcher.utter_message(response="utter_user_not_ready")
        else:
            dispatcher.utter_message(text="No entendí tu respuesta, ¿puedes repetirla?")

        return []

class ActionCheckUserStatus(Action):
    def name(self) -> Text:
        return "action_check_user_status"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_status = tracker.get_slot("user_status")

        if user_status == "true":
            dispatcher.utter_message(response="utter_user_status_ok")
        elif user_status == "false":
            dispatcher.utter_message(response="utter_user_status_not_yet")
        else:
            dispatcher.utter_message(text="No entendí tu respuesta, ¿puedes repetirla?")

        return []