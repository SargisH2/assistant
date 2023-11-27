import os
import json
import requests
from serpapi import GoogleSearch
import json
import time
from openai import OpenAI

ASSISTANT_ID = 'asst_Uqqdh4SU7KUxEhA9TZteDAiK'

client = OpenAI()
assistant = client.beta.assistants.retrieve(ASSISTANT_ID)


SERPAPI_API_KEY = os.environ['SERPAPI_API_KEY']


def google_search(query):
    print('Google search:', query)
    params = {
      "engine": "google",
      "q": query,
      "google_domain": "google.com",
      "api_key": SERPAPI_API_KEY
    }
    search = GoogleSearch(params)
    return search.get_dict() 
google_search_json = {
    "name": "google_search",
    "description": "Search query in google",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {"type": "string"}
        },
        "required": ["query"],
    },
}


def ebay_search(query):
    print('Ebay search:', query)
    params = {
      "engine": "ebay",
      "_nkw": query,
      "ebay_domain": "ebay.com",
      "api_key": SERPAPI_API_KEY
    }
    search = GoogleSearch(params)
    return search.get_dict()
ebay_search_json = {
    "name": "ebay_search",
    "description": "Search in Ebuy with SerpAPI",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {"type": "string"}
        },
        "required": ["query"],
    },
}

def get_similarity(url1, url2):
    print("Getting scores...")
    url = 'https://imgsimilarityapi.azurewebsites.net/apiv1/'
    body = {
        "url1": url1,
        "url2": url2
    }
    try:
        x = requests.post(url, json = body)
        result = json.loads(x.text)['score'][0]
        return result
    except Exception as e:
        print("Error while getting similarity scores:", e)
        print(body)
get_similarity_json = {
    "name": "get_similarity",
    "description": "Get similarity score of 2 images from urls. Score is a float number between 0 and 1.",
    "parameters": {
        "type": "object",
        "properties": {
            "url1": {"type": "string"},
            "url2": {"type": "string"}
        },
        "required": ["url1", "url2"],
    },
}

############################################### Work with Assistant

def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.3)
    return run



def run_thread(thread):
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id = ASSISTANT_ID
    )
    run = wait_on_run(run, thread)
    while run.status == 'requires_action':
        tool_calls = run.required_action.submit_tool_outputs.tool_calls
        call_ids = []
        call_outputs = []
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            search_result = eval(function_name)(**arguments)

            call_outputs.append(json.dumps(search_result))
            call_ids.append(tool_call.id)


            # if tool_call.function.name == 'google_search':
            #     arguments = json.loads(tool_call.function.arguments)
            #     search_result = google_search(arguments['query'])
                
            #     call_outputs.append(json.dumps(search_result))
            #     call_ids.append(tool_call.id)
                
        run = client.beta.threads.runs.submit_tool_outputs(
            thread_id = thread.id,
            run_id = run.id,
            tool_outputs =
            [
                {
                    "tool_call_id": id,
                    "output": output,
                } for id, output in zip(call_ids, call_outputs)
            ],
        )
        run = wait_on_run(run, thread)

        
def handle(query: str, id: str = '') -> tuple:
    if id == '':
        thread = client.beta.threads.create()
        id = thread.id
    else:
        try:
            thread = client.beta.threads.retrieve(id)
        except:
            print('Invalid id. Creating new conversation')
            thread = client.beta.threads.create()
            id = thread.id
    client.beta.threads.messages.create(
        thread_id = id,
        role = "user",
        content = query
    )
    run_thread(thread)
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    ).data
    return id, list(map(lambda message: {message.role: message.content[0].text.value}, reversed(messages)))