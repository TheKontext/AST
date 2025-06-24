import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()


FOLDER_ID = os.getenv('FOLDER')  # Идентификатор каталога Yandex Cloud
API_KEY = os.getenv('API')  # API-ключ сервисного аккаунта
MODEL_NAME = "yandexgpt-lite"  # Выбор модели: yandexgpt-lite или yandexgpt
MAX_HISTORY = 6  # Максимальное количество сообщений в контексте


def main(message):
    text = '''
    я отправил тебе анкету, тебе нужно составить несколько  вопросов, направленых на профорентацию,
     учти что твой ответ должен содержать ТОЛЬКО вопросы: 
    '''
    messages = [
        {"role": "user", "text": text + message}
    ]


    request_body = {
            "modelUri": f"gpt://{FOLDER_ID}/{MODEL_NAME}",
            "completionOptions": {
                "stream": False,
                "temperature": 0.6,
                "maxTokens": "2000"
            },
            "messages": messages
        }

    headers = {
        "Authorization": f"Api-Key {API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(
                "https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
                headers=headers,
                json=request_body
            )
    data = response.json()
    #print(json.dumps(data, indent=4))
    return data['result']['alternatives'][0]['message']['text']

def ans(message):
    text = '''
    я отправлю тебе ряд вопросов и фактов о человеке,на их основе отправь Только ряд профессий(2-5 штук), которые могут подойти этому человеку,
     с их небольшим описанием, выдели названия проффессий в <b></b>: 
    '''
    messages = [
        {"role": "user", "text": text + message}
    ]


    request_body = {
            "modelUri": f"gpt://{FOLDER_ID}/{MODEL_NAME}",
            "completionOptions": {
                "stream": False,
                "temperature": 0.6,
                "maxTokens": "2000"
            },
            "messages": messages
        }

    headers = {
        "Authorization": f"Api-Key {API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(
                "https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
                headers=headers,
                json=request_body
            )
    data = response.json()
    #print(json.dumps(data, indent=4))
    return data['result']['alternatives'][0]['message']['text']