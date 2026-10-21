from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")

async def generate_response(message: str) -> str:
    response = await model.ainvoke(message)
    content = response.content[0]["text"] 
    
    if isinstance(content, str):
        return content
    
    if isinstance(content, list):
        return "\n".join(block["text"] for block in content if isinstance(block, dict) and "text" in block)
    
    return str(content)
    
    
    