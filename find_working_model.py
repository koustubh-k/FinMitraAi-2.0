import os
import sys
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
load_dotenv(env_path)

groq_models = ["gemma2-9b-it", "llama3-70b-8192", "mixtral-8x7b-32768", "llama3-8b-8192", "llama-3.3-70b-versatile", "llama-3.1-8b-instant", "llama3-groq-70b-8192-tool-use-preview"]
gemini_models = ["gemini-pro", "gemini-1.5-pro", "gemini-1.5-flash", "gemini-1.0-pro"]
mistral_models = ["open-mistral-7b", "mistral-small-latest", "open-mixtral-8x7b"]

working_provider = None
working_model = None

from langchain_mistralai import ChatMistralAI
for m in mistral_models:
    try:
        print(f"Testing mistral {m}...")
        llm = ChatMistralAI(model=m)
        res = llm.invoke("Hi")
        print(f"SUCCESS Mistral: {m}")
        working_provider = "mistral"
        working_model = m
        break
    except Exception as e:
        print(f"Failed {m}: {e}")

if not working_provider:
    from langchain_groq import ChatGroq
    for m in groq_models:

if not working_provider:
    from langchain_google_genai import ChatGoogleGenerativeAI
    for m in gemini_models:
        try:
            print(f"Testing gemini {m}...")
            llm = ChatGoogleGenerativeAI(model=m)
            res = llm.invoke("Hi")
            print(f"SUCCESS Gemini: {m}")
            working_provider = "gemini"
            working_model = m
            break
        except Exception as e:
            print(f"Failed {m}: {e}")

if not working_provider:
    from langchain_mistralai import ChatMistralAI
    for m in mistral_models:
        try:
            print(f"Testing mistral {m}...")
            llm = ChatMistralAI(model=m)
            res = llm.invoke("Hi")
            print(f"SUCCESS Mistral: {m}")
            working_provider = "mistral"
            working_model = m
            break
        except Exception as e:
            print(f"Failed {m}: {e}")

if working_provider:
    print(f"\nFOUND WORKING: {working_provider} with {working_model}")
else:
    print("\nNO WORKING MODELS FOUND across all keys.")
