import asyncio
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from fastapi import FastAPI

load_dotenv()

app = FastAPI(
    title="Gemini API"
)

async def gemini_response():
    model = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite",
        temperature=0.4
    )
    response = await model.ainvoke("Hello Gemini!")
    print(response.content[0]["text"])

asyncio.run(gemini_response())
