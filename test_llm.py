import asyncio
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

async def gemini_response():
    model = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite",
        temperature=0.4
    )
    response = await model.ainvoke("Hello Gemini!")
    print(response.content[0]["text"])

asyncio.run(gemini_response())