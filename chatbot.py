import requests
import wolframalpha
import openai
import re
from APIKeys import WOLFRAM_APP_ID, OPENAI_API_KEY

# Wolframalpha credentials
client = wolframalpha.Client(WOLFRAM_APP_ID)

# OpenAI credentials
openai.api_key = OPENAI_API_KEY


def GPTQuery(myInput):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.5,
        max_tokens=256,
        # n=3,
        messages=[
            {"role": "system", "content": "You are a helpful assistant. However, if you're asked to provide an answer "
                                          "to a purely factual or analytical question that could reasonably be "
                                          "answered by Wolfram Alpha, delegate to Wolfram Alpha instead by outputting "
                                          "a query that Wolfram Alpha would understand. Indicate this scenario by "
                                          "formatting the output exactly like this: Query for WolframAlpha: <query>"},
            {"role": "user", "content": myInput},
        ]

    )
    return completion.choices[0].message.content


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
        return f"Wolfram: {response.text}"
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
            myResponse = GPTQuery(promptNew)
            print(f"ChatGPT: {myResponse}")


if __name__ == "__main__":
    chatbot()
