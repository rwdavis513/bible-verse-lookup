import requests
from lex_interface import close, elicit_slot


def look_up_verse(intent_request):
    """
    Pulls the bible verse given the intent request.

    :param intent_request:
    :return:
    """
    session_attributes = intent_request['sessionAttributes']

    if 'slots' in intent_request.keys():
        slots = intent_request['slots']
    else:
        return elicit_slot(session_attributes=session_attributes,
                           slot_to_elicit='Book'
                           )

