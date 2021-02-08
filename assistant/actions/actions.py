import logging
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset, SlotSet, EventType, SessionStarted, ActionExecuted
import pandas as pd

class IncidentStatus(Action):

    def name(self):
        return 'action_incident_status'

    def run(self, dispatcher, tracker, domain):

        data = pd.read_csv('workshop_data.csv')
        user_id = tracker.get_slot('number')

        find_user = data.loc[data['user_id']==user_id]

        status = find_user.incident_number_status.values[0]
        email = find_user.email.values[0]

        dispatcher.utter_message("The status of your ticket is : {}".format(status))

        return [SlotSet("email", email)]

