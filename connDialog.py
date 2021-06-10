# -*- coding: utf-8 -*-

import os
import dialogflow
from google.api_core.exceptions import InvalidArgument

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'private_key.json'

DIALOGFLOW_PROJECT_ID = 'newagent-poqi'
DIALOGFLOW_LANGUAGE_CODE = 'it'
SESSION_ID = 'me'


def invioMessaggioAgente(inputUtente):
        text_to_be_analyzed = inputUtente
        
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
        text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
        query_input = dialogflow.types.QueryInput(text=text_input)
        try:
            response = session_client.detect_intent(session=session, query_input=query_input)
        except InvalidArgument:
            raise
        
        return response.query_result.fulfillment_text
    