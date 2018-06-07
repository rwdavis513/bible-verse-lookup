import requests
import config
from lex_interface import close, elicit_slot, delegate


def validate_slots(slots):
    """

    :param slots:
    :return:
    """
    keys = ['Book', 'chapter', 'verse']
    return [ slots[key] for key in keys]


def query_bible_api(book=None, chapter=None, verse=None):
    """
    Queries the esv API
    :param book:
    :param chapter:
    :param verse:
    :return:
    """
    API_URL = "https://api.esv.org/v3/passage/text/?q="
    query_string = API_URL + book + ' ' + str(chapter) + ':' + str(verse)
    result = requests.get(query_string, headers={'Authorization': 'Token ' + config.ESV_API_KEY})
    if result.status_code == 200:
        data = result.json()
        return data['passages'][0]


def look_up_verse(intent_request):
    """
    Pulls the bible verse given the intent request.

    :param intent_request:
    :return:
    """
    session_attributes = intent_request['sessionAttributes']
    confirmation_status = intent_request['currentIntent']['confirmationStatus']
    if 'slots' in intent_request['currentIntent'].keys():
        slots = intent_request['currentIntent']['slots']
    else:
        return elicit_slot(session_attributes=session_attributes,
                           slot_to_elicit='Book',
                           intent_name="LookUpVerse",
                           slots=None,
                           message="Which book which you look to look up?"
                           )

    invocation_status = intent_request['invocationSource']  # 'DialogCodeHook', ReadyForFulfillment

    if invocation_status == 'FulfillmentCodeHook' or invocation_status == 'ReadyForFulfillment':
        try:
            book, chapter, verse = validate_slots(slots)
        except KeyError as e:
            return elicit_slot(slot_to_elicit=e.args[0],
                               session_attributes=session_attributes,
                               intent_name="LookUpVerse",
                               slots=None,
                               message="Which book which you look to look up?"
                               )

        passage_result = query_bible_api(**{'book': book,
                                          'chapter': chapter,
                                          'verse': verse }
                                         )
        if passage_result:
            return close(session_attributes,
                         'Fulfilled',
                         passage_result,
                         )
    else:
        return delegate(session_attributes, slots)
