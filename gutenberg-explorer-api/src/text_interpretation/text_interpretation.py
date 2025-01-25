from fastapi import FastAPI, status, Response, Request
import openai
import json

analyze_text_sub_app = FastAPI()

@analyze_text_sub_app.post("/", status_code=200)
async def analyse_text(response: Response, request: Request):
    '''
    Analyze text From Gutenberg book
    '''
    try:
        print("test")
        data = await request.body()
        data = json.loads(data)
        if not data["data"]:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"message": "Invalid Payload"}

        text = data["data"]

        summary_prompt = f"Summarize the following text:\n\n{text}"
        summary_response = openai.completions.create(
            engine="text-davinci-003",
            prompt=summary_prompt,
            max_tokens=150
        )
        character_prompt = f"Identify the principal characters in the following text:\n\n{text}"
        character_response = openai.completions.create(
            engine="text-davinci-003",
            prompt=character_prompt,
            max_tokens=150
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
