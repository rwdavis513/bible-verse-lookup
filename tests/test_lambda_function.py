from app.lambda_function import lambda_handler


context = None

default_input_from_lex = {
        "sessionAttributes": {
        },
        "currentIntent": {
            "name": "LookUpVerse",
            "slots": {
                "Book": "Joshua"
            },
            "confirmationStatus": "None"
        },
        "inputTranscript": "Next Card",
        "messageVersion": "1.0",
        "invocationSource": "DialogCodeHook",
        "userId": "c137b82f-beaf-431e-b795-4f256785e507:T8W5HFZK7:U8VFKR2AV",
        "requestAttributes": {
            "x-amz-lex:accept-content-types": "PlainText",
            "x-amz-lex:channel-name": "SlackDevelopment",
            "x-amz-lex:channel-type": "Slack"
        },
        "bot": {
            "name": "BibleVerseLookup",
            "alias": "MTTBotDevelopment",
            "version": "5"
        },
        "outputDialogMode": "Text"
}


def test_lambda_handler():
    resp = lambda_handler(default_input_from_lex, context)
    assert type(resp) == dict


def test_lambda_handler_fullfillment():
    default_input_from_lex['invocationSource'] = 'FulfillmentCodeHook'
    default_input_from_lex['currentIntent']['slots']['chapter'] = '5'
    #default_input_from_lex['currentIntent']['slots']['verse'] = '8'
    resp = lambda_handler(default_input_from_lex, context)
    assert type(resp) == dict
