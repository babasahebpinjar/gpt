# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


from rasa.core.channels.channel import InputChannel
from rasa.core.channels.rest import RestInput
from flask import Blueprint, request, jsonify

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from typing import Any, Dict, List, Text, Union
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict


from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

import json


class ActionRetrieveSlots(Action):
    def name(self) -> Text:
        return "action_retrieve_slots"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        json_payload = tracker.latest_message.get("text")
        if not json_payload:
            print("No JSON payload found")
            return []
        try:
            slot_values = json.loads(json_payload)
        except json.decoder.JSONDecodeError as e:
            print(f"Error decoding JSON payload: {e}")
            return []
        events = []
        for slot_name, slot_value in slot_values.items():
            events.append(SlotSet(slot_name, slot_value))
            print(f"Retrieved slot {slot_name}: {slot_value}")
        return events

class ActionGreet(Action):
    def name(self) -> Text:
        return "action_greet"

    
    # def run(self, dispatcher: CollectingDispatcher,
    #         tracker: Tracker,
    #         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
        **kwargs: Any,
    ) -> List[Dict[Text, Any]]:
        payload = kwargs.get("payload", {})
        slots = payload.get("slots", {})
        
    # def run(
    #         self,
    #         dispatcher: CollectingDispatcher,
    #         tracker: Tracker,
    #         domain: Dict[Text, Any],
    #         payload: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    # def run(self, dispatcher: CollectingDispatcher,
    #         tracker: Tracker,
    #         domain: Dict[Text, Any],
    #         payload: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        

        #slots = payload.get("slots", {})
        #dispatcher.utter_message(template="utter_welcome_back")
        
        json_payload = tracker.latest_message.get("text","")
        print(f"Received JSON payload: {json_payload}")
        slot_value = tracker.get_slot("location")
        print(f"Received location payload: {slot_value}")
        
        
        latest_message = tracker.latest_message
        
        # Convert the message to a JSON string
        message_json = json.dumps(latest_message, indent=4)
        
        # Print the JSON string to the console
        print(message_json)
        
        if not json_payload:
            print("No JSON payload found")
            return []
        try:
            slot_values = json.loads(json_payload)
        except json.decoder.JSONDecodeError as e:
            print(f"Error decoding JSON payload: {e}")
            return []
        events = []
        for slot_name, slot_value in slot_values.items():
            events.append(SlotSet(slot_name, slot_value))
        print(f"Received JSON payload: {json_payload}")
        
        
        latest_message = tracker.latest_message
        print("full message is : ",latest_message)
        message = latest_message.get("text")
        payload = latest_message.get("payload", {})
        slots = payload.get("slots", {})
        
        
        #origin = slots.get("origin")
        #location = slots.get("location")
        
        
        #slots = payload.get("slots", {})
        #origin = slots.get("origin")
        location = slots.get("location")
        print("Location is : " ,tracker.get_slot('location'),location)
        
        # greeted = tracker.get_slot("greeted")
        # if greeted:
        #     dispatcher.utter_message(template="utter_welcome_back")
        # else:
        #     dispatcher.utter_message(template="utter_greet")
        #     tracker.slots["greeted"] = True
        
        greeted = tracker.get_slot("location")
        if location == "New york":
            dispatcher.utter_message(template="utter_happy")
        else:
            dispatcher.utter_message(template="utter_did_that_help")
            #tracker.slots["greeted"] = True
            tracker.slots["location"] = location
            
        # Set the slot values in the tracker
        return [
            #SlotSet("origin", origin),
            SlotSet("location", location),
            #SlotSet("date", date),
        ]
        #return []

class ActionBookFlight(Action):
    def name(self) -> Text:
        return "action_book_flight"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        greeted = tracker.get_slot("greeted")
        location = tracker.get_slot("location")
        #departure_date = tracker.get_slot("departure_date")

        print("Values are : ",greeted,location)
        dispatcher.utter_message(template="utter_happy")
        # do something with the slot values...

        return []


class ActionGoodbye(Action):
    def name(self) -> Text:
        return "action_goodbye"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(template="utter_goodbye")
        
        return []

class JsonInput(InputChannel):
    
    @staticmethod
    def _extract_sender(request):
        return request.json.get("sender", None)

    @staticmethod
    def _extract_message(request):
        return request.json.get("message", None)

    @staticmethod
    def _extract_metadata(request):
        return request.json.get("metadata", None)

    def blueprint(self, on_new_message):
        json_webhook = Blueprint('json_webhook', __name__)

        @json_webhook.route("/", methods=['POST'])
        def receive():
            sender_id = self._extract_sender(request)
            message = self._extract_message(request)
            metadata = self._extract_metadata(request)

            # Custom code to handle the incoming message
            # and pass it to the on_new_message callback function

            
            return jsonify({"status": "success"})
        #print("The message is : ---- ", metadata)
        return [json_webhook]




class SetSlotValuesFromJson(Action):
    def name(self) -> Text:
        return "action_set_slot_values_from_json"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:

        #dispatcher.utter_message(text="Hello from json channel!..!")
        #dispatcher.utter_template("utter_happy", tracker)
        dispatcher.utter_message(template="utter_welcome_back")
        # Get the latest user message
        latest_message = tracker.latest_message

        # Get the message text and extract slot values from the JSON payload
        message = latest_message.get("text")
        payload = latest_message.get("payload", {})
        slots = payload.get("slots", {})
        #origin = slots.get("origin")
        location = slots.get("location")
        if location == 'New york':   
            #date = slots.get("date")        
            dispatcher.utter_message(text="Hello from json channel!")
            dispatcher.utter_template("utter_happy", tracker)  # calling an utterance template


        # Set the slot values in the tracker
        return [
            #SlotSet("origin", origin),
            SlotSet("location", destination),
            #SlotSet("date", date),
        ]
