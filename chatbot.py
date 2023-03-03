import requests
import wolframalpha
import openai
import re
from APIKeys import WOLFRAM_APP_ID, OPENAI_API_KEY

# Wolframalpha credentials
client = wolframalpha.Client(WOLFRAM_APP_ID)

# OpenAI credentials
openai.api_key = OPENAI_API_KEY


# This function processes user input through the ChatGPT API
def GPTQuery(myInput):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.2,   # Lower temperature values make the output less random
        max_tokens=256,
        # Instruct the model on how to process certain inputs:
        messages=[
            {"role": "system", "content": "You are a helpful assistant. However, if you're asked to provide an answer "
                                          "to a calculation or purely factual or analytical question that could "
                                          "reasonably be answered by Wolfram Alpha, delegate to Wolfram Alpha instead "
                                          "by outputting a query that Wolfram Alpha would understand. Indicate this "
                                          "scenario by formatting the output exactly like this: Query for "
                                          "WolframAlpha: <query>"},
            {"role": "user", "content": myInput},
        ]

    )

    chatGPTresponse = completion.choices[0].message.content

    # Checks to see if ChatGPT's response needs to be passed to Wolfram Alpha
    if "Query for WolframAlpha:" in chatGPTresponse:
        properWolframQuery = chatGPTresponse.replace("Query for WolframAlpha:", "")
        return wolframQuery(properWolframQuery)
    # If not, return ChatGPT's response
    else:
        return chatGPTresponse


# This function processes queries through the Wolfram Alpha Short Answers API
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
        return f"According to Wolfram Alpha, {response.text}"
    else:
        # Print the error message returned by the API
        return f"Error: {response.text}"


def chatbot():
    while True:
        prompt = input("You: ")
        promptNew = prompt.lower()

        # Allows the user to override ChatGPT processing and process through Wolfram Alpha if a basic calculation is
        # entered or the user adds the word "wolfram" to their query
        if re.search(r"(\d+[\+\-\*\/])+\d+", promptNew) or "wolfram" in promptNew:
            result = wolframQuery(promptNew)
            print(result)

        else:
            myResponse = GPTQuery(promptNew)
            print(f"ChatGPT: {myResponse}")


if __name__ == "__main__":
    chatbot()
