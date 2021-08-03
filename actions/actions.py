# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from rasa_sdk import Action
from rasa_sdk.events import SlotSet, AllSlotsReset
import requests
import json
from random import randint
import datetime
import os
import yaml

from database_connector import DataUpdate

class ActionSearchRestaurant(Action):

    def name(self) -> Text:
        return "action_search_restaurant"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Please temporarily ask google https://google.com, we will search for you then")

        return []


class ActionPlaceSearch(Action):
    def name(self):
        # define the name of the action
        return 'action_place_search'

    def run(self, dispatcher, tracker, domain):
        # retrieve slot values
        query = tracker.get_slot('query')
        radius = tracker.get_slot('number')
        print("radius", radius)
        print("query", query)

        # retrieve google api key
        with open("./ga_credentials.yml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
        key = cfg['credentials']['GOOGLE_KEY']

        # get user's current location
        get_origin = requests.post(
            "https://www.googleapis.com/geolocation/v1/geolocate?key={}".format(key)).json()
        print(get_origin)
        origin_lat = get_origin['location']['lat']
        origin_lng = get_origin['location']['lng']

        # look for a place using all the details
        print("origin_lat", origin_lat)
        print("origin_lng", origin_lng)
        print("radius", radius)
        print("query", query)
        place = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={},{}&radius={}&type={}&key={}".format(origin_lat, origin_lng, radius, query, key)).json()
        if len(place['results']) == 0:
            dispatcher.utter_message("Sorry, I didn't find anything")
            return [SlotSet('location_match', 'none')]
        else:
            for i in place['results']:
                if 'rating' and 'vicinity' in i.keys():
                    if 'rating' not in i.keys():
                        continue
                    else:
                        rating = i['rating']

                    name = i['name']
                    address = i['vicinity']
                    print(name)
                    print(rating)
                    print(address)

                    if 'opening_hours' not in i.keys():
                        opening_hours = 'open'
                    else:
                        if (i['opening_hours']['open_now'] == True):
                            opening_hours = 'open'
                        else:
                            opening_hours = 'closed'
                        break
        speech = "I found a {} called {} based on your specified parameters.".format(query, name)
        dispatcher.utter_message(speech)  # send the response back to the user
        return [SlotSet('location_match', 'one'), SlotSet('rating', rating), SlotSet('address', address),
                SlotSet('opening_hours', opening_hours)]  # set returned details as slots

class ActionLastName(Action):
    def name(self):
        # define the name of the action
        return 'action_last_name'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(template="utter_last_name")
        return[SlotSet('firstN', tracker.latest_message['text'])]

class ActionFeedback(Action):
    def name(self):
        # define the name of the action
        return 'action_feedback'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(template="utter_feedback")
        return[SlotSet('lastN', tracker.latest_message['text'])]

class ActionSubmit(Action):
    def name(self):
        # define the name of the action
        return 'action_submit'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="Your first name is {0}, your lastname is {1} and your feedback is {2}. Thank you! Have a nice day!".format(tracker.get_slot("firstN"), tracker.get_slot("lastN"), tracker.get_slot("feedback")))
        DataUpdate(tracker.get_slot("firstN"), tracker.get_slot("lastN"), tracker.get_slot("feedback"))
        dispatcher.utter_message("Thanks for your feedback!")
        return[]