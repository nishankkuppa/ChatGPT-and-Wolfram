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
        temperature=0.2,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response["choices"][0]["text"]


def CalculationQuery(calc):
    res = client.query(calc)
    answer = next(res.results).text
    return answer


def chatbot():
    while True:
        prompt = input("You: ")
        # Check if the input is a calculation
        # if "=" in prompt or "+" in prompt or "-" in prompt or "*" in prompt or "/" in prompt:
        if re.search(r"(\d+[\+\-\*\/])+\d+", prompt):
            result = CalculationQuery(prompt)
            print("Wolfram: The result is " + str(result))
        else:
            myResponse = openAIQuery(prompt)
            print("OpenAI: " + myResponse)

if __name__ == "__main__":
    chatbot()
