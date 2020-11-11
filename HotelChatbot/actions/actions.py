# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List, Union
from rasa_sdk.events import SlotSet, UserUtteranceReverted
import datetime
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.forms import FormAction
#
def repeat(tracker, dispatcher):
    user_ignore_count = 2
    count = 0
    tracker_list = []

    while user_ignore_count > 0:
        event = tracker.events[count].get('event')
        if event == 'user':
            user_ignore_count = user_ignore_count - 1
        if event == 'bot':
            tracker_list.append(tracker.events[count])
        count = count - 1

    tracker_list.reverse()
    i = len(tracker_list) - 1

    while i >= 0:
        data = tracker_list[i].get('data')
        if data:
            if "buttons" in data:
                dispatcher.utter_message(text=tracker_list[i].get('text'), buttons=data["buttons"])
            else:
                dispatcher.utter_message(text=tracker_list[i].get('text'))
            break
        i -= 1

class ActionSelectRoom(Action):
    def name(self):
        return 'action_select_room'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(template="utter_room_submit")
        return []

class ActionRelativeTime(Action):
    def name(self):
        return 'action_relative_time'

    def run(self, dispatcher, tracker, domain):
        time = tracker.get_slot("time")
        if(time['to'] == None):
            set_time = datetime.datetime.strptime(str(time['from']), '%Y-%m-%dT%H:%M:%S.%f%z')
            original_time = set_time.strftime("%H:%M %p %d, %b, %Y")
            # set_time = time['from']
        elif(time['from'] == None):
            set_time = datetime.datetime.strptime(str(time['to']), '%Y-%m-%dT%H:%M:%S.%f%z')
            original_time = set_time.strftime("%H:%M %p %d, %b, %Y")
            # set_time = time['to']
        dispatcher.utter_message(template="utter_room_clean_schedule_timings", time= original_time)
        return []
    

class ActionCheckInTime(Action):
    
    def name(self):
        return "action_checkin_time"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template("utter_faq_checkin_time", tracker)
        repeat(tracker, dispatcher)        
        return [UserUtteranceReverted()]

class ActionCheckOutTime(Action):
    
    def name(self):
        return "action_checkout_time"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template("utter_faq_checkout_time", tracker)
        repeat(tracker, dispatcher)
        return [UserUtteranceReverted()]
    
class ActionCancelReservation(Action):
    
    def name(self):
        return "action_cancel_reservation"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template("utter_faq_cancel_reservation", tracker)
        repeat(tracker, dispatcher)
        return [UserUtteranceReverted()]

class ActionCancellationPolicy(Action):
    
    def name(self):
        return "action_cancellation_policy"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template("utter_faq_cancellation_policy", tracker)
        repeat(tracker, dispatcher)
        return [UserUtteranceReverted()]

class ActionHaveRestaurant(Action):
    
    def name(self):
        return "action_restaurant_availability"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template("utter_faq_restaurant_availability", tracker)
        repeat(tracker, dispatcher)
        return [UserUtteranceReverted()]

class ActionBreakfastAvail(Action):
    
    def name(self):
        return "action_breakfast_availability"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template("utter_faq_breakfast_availability", tracker)
        repeat(tracker, dispatcher)
        return [UserUtteranceReverted()]
    
class ActionBreakfastTime(Action):
    
    def name(self):
        return "action_breakfast_time"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template("utter_faq_breakfast_time", tracker)
        repeat(tracker, dispatcher)
        return [UserUtteranceReverted()]

class ActionRestaurantTime(Action):
    
    def name(self):
        return "action_restaurant_timings"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template("utter_faq_restaurant_timings", tracker)
        repeat(tracker, dispatcher)
        return [UserUtteranceReverted()]