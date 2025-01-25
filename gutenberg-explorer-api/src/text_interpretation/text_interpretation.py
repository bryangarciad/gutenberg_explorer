from fastapi import FastAPI, status, Response, Request
from openai import OpenAI
import json

analyze_text_sub_app = FastAPI()

@analyze_text_sub_app.post("/", status_code=200)
async def analyse_text(response: Response, request: Request):
    '''
    Analyze text From Gutenberg book
    '''
    try:
        data = await request.body()
        data = json.loads(data)
        if not data["data"]:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"message": "Invalid Payload"}

        text = data["data"]

        summary_prompt = f"Summarize the following text:\n\n{text}"
        client = OpenAI()
        summary_response = client.completions.create(
            model="gpt-4o-mini",
            prompt=summary_prompt,
            max_tokens=3000
        )
        character_prompt = f"Identify the principal characters in the following text:\n\n{text}"
        character_response = client.completions.create(
            model="gpt-4o-mini",
            prompt=character_prompt,
            max_tokens=3000
        )
        characters = character_response.choices[0].text.strip()
        summary = summary_response.choices[0].text.strip()

        return {"data": {
            characters: characters,
            summary: summary
        }}
    except Exception as _:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": "Something went wrong"}
