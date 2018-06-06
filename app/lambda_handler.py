import traceback
import time
import os

from config import logger
from lex_interface import build_validation_result, try_ex, close, elicit_slot
from bible_interface import look_up_verse


def welcome_message(intent_request):
    """
    Replies to someone saying hi.
    """

    if intent_request['sessionAttributes'] is not None:
        session_attributes = intent_request['sessionAttributes']
        if type(session_attributes) == dict and 'count' in session_attributes.keys():
            session_attributes['count'] = int(session_attributes['count']) + 1
        else:
            session_attributes['count'] = 1
    else:
        session_attributes = {}
        session_attributes['count'] = 0

    if session_attributes['count'] > 1:
        message = "How can I help you?"
    else:
        message = "Hi! I'm your bot. I'm here to do ..."

    if intent_request['invocationSource'] == 'FulfillmentCodeHook':
        return close(session_attributes,
                         'Fulfilled',
                         {
                             'contentType': 'PlainText',
                             'content': message
                         }
                    )


def good_bye(intent_request):
    """
    Replies to someone saying hi.
    """

    if intent_request['sessionAttributes'] is not None:
        session_attributes = intent_request['sessionAttributes']
        if type(session_attributes) == dict and 'count' in session_attributes.keys():
            session_attributes['count'] = int(session_attributes['count']) + 1
        else:
            session_attributes['count'] = 1


    message = "Farewell! Please come again soon!"

    if intent_request['invocationSource'] == 'FulfillmentCodeHook':
        return close(session_attributes,
                         'Fulfilled',
                         {
                             'contentType': 'PlainText',
                             'content': message
                         }
                    )


def help_message(intent_request):
    """
    Replies to someone saying hi.
    """

    if intent_request['sessionAttributes'] is not None:
        session_attributes = intent_request['sessionAttributes']
        if type(session_attributes) == dict and 'count' in session_attributes.keys():
            session_attributes['count'] = int(session_attributes['count']) + 1
        else:
            session_attributes['count'] = 1
    else:
        session_attributes = {}

    if session_attributes['count'] > 1:
        message = "Right now we can help you learn the machine codes you need for your class."
    else:
        message = "Ok Great!"

    if intent_request['invocationSource'] == 'FulfillmentCodeHook':
        return elicit_slot(session_attributes,
                         'FindMachineCode',
                         {'MachineCodeCue': None},
                         'MachineCodeCue',
                         {
                             'contentType': 'PlainText',
                             'content': message
                         }
                    )


# keys = intent, value = function to call
# intent_name : intent_function
intent_functions = {
    'LookUpVerse': look_up_verse,
    'HelpMessage': help_message,
    'Welcome': welcome_message
}


# --- Intents ---
def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """
    logger.debug(
        'dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))
    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    try:
        return intent_functions[intent_name](intent_request)
    except KeyError:
        raise Exception('Intent with name ' + intent_name + ' not supported')


# --- Main handler ---
def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    # By default, treat the user request as coming from the America/New_York time zone.
    os.environ['TZ'] = 'America/Denver'
    time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))
    logger.debug(event)
    session_attributes = event['sessionAttributes']
    try:
        response = dispatch(event)
    except Exception as e:
        logger.error(e)
        logger.error(traceback.print_exc())
        message = {
            'contentType': 'PlainText',
            'content': "Oops! We had an error. Please pass this message to tech support: {}".format(e)
        }
        response = close(session_attributes, 'Fulfilled', message)
    return response