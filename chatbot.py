import requests
import wolframalpha
import openai
import re
from APIKeys import WOLFRAM_APP_ID, OPENAI_API_KEY

# Wolframalpha credentials

client = wolframalpha.Client(WOLFRAM_APP_ID)

# OpenAI credentials
openai_url = "https://api.openai.com/v1/engines/davinci/jobs"
openai.api_key = OPENAI_API_KEY


def openAIQuery(text):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=text,
        temperature=0.5,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response["choices"][0]["text"].replace('\n', '')


def CalculationQuery(calc):
    res = client.query(calc)
    answer = next(res.results).text
    return answer


def wolframQuery(userInput):
    # Define the API endpoint URL and the query parameters
    api_url = "https://api.wolframalpha.com/v1/spoken"
    params = {
        "appid": WOLFRAM_APP_ID,
        "i": userInput
    }
    # Send the HTTP request to the API endpoint
    response = requests.get(api_url, params=params)
    # Check if the request was successful (i.e., HTTP status code 200)
    if response.status_code == 200:
        # Print the short answer returned by the API
        return "Wolfram: " + response.text
    else:
        # Print the error message returned by the API
        return f"Error: {response.text}"


def chatbot():
    while True:
        prompt = input("You: ")
        promptNew = prompt.lower()

        # Check if the input is a calculation
        # if "=" in prompt or "+" in prompt or "-" in prompt or "*" in prompt or "/" in prompt:
        if re.search(r"(\d+[\+\-\*\/])+\d+", promptNew) or "wolfram" in promptNew:
            result = wolframQuery(promptNew)
            print(result)

        else:
            myResponse = openAIQuery(promptNew)
            print("OpenAI: " + myResponse)


if __name__ == "__main__":
    chatbot()
