"""
Step 2:
Text Generation using Gemini API
generate API key from: https://ai.google.dev/gemini-api/docs/api-key
"""

from google import genai

client = genai.Client(api_key="AIzaSyCKTzb2ssRplrWe8ZZ0D-PuvXddeRRtArU")

def gemini_api(text):
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=text
    )

    print(response.text)


# -------------MAIN----------------

text = "Hi, be my personal AI robot. explain to me what an api is briefly?"
gemini_api(text)
