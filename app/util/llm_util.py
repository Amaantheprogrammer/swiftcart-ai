from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from app.util.env_util import GEMINI_MODEL

load_dotenv()

model = ChatGoogleGenerativeAI(
    model=GEMINI_MODEL
)

llm = model | StrOutputParser()