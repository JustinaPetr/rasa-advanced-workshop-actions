import logging
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset, SlotSet, EventType, SessionStarted, ActionExecuted
from rasa_sdk.forms import FormAction, FormValidationAction, REQUESTED_SLOT
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


class OpenIncident(Action):

    def name(self):
        return 'action_open_incident'

    def run(self, dispatcher, tracker, domain):

        incident_title = tracker.get_slot('incident_title')
        dispatcher.utter_message("The ticket for your problem {} has been opened.".format(incident_title))

        return []


class ValidateOpenIncidentForm(FormValidationAction):

    def name(self):
        return 'validate_open_incident_form'

    def validate_problem_description(self, slot_value, dispatcher, tracker, domain):

        if len(slot_value.split())>1:
            return {"problem_description": slot_value}
        else:
            dispatcher.utter_message("The description is too short. Please rephrase")
            return {"problem_description": None}