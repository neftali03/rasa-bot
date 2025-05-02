from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class ActionHandleGreetings(Action):
    def name (self) -> Text:
        return "action_handle_greetings"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        current_count = tracker.get_slot("greetings_count") or 0
        new_count = current_count + 1

        if new_count > 1:
            dispatcher.utter_message(response="utter_greetings_extra")
        else:
            dispatcher.utter_message(response="utter_greetings")

        return [SlotSet("greetings_count", new_count)]

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

        return []