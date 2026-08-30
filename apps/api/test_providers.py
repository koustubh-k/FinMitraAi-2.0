import os
import sys

# Flush output automatically
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

from dotenv import load_dotenv

# Load env
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.env')
print(f"Loading env from {env_path}")
load_dotenv(env_path)

# Add apps/api to path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__))))

from app.agents.nodes import _get_llm
from app.providers.market.registry import provider_registry

def test_llms():
    print("Testing LLMs...")
    providers = ["mistral"]
    for p in providers:
        try:
            print(f"Testing {p}...")
            os.environ["LLM_PROVIDER"] = p
            llm = _get_llm(p)
            res = llm.invoke("Hello, say 'Test successful'.")
            print(f"[OK] {p}: {res.content}")
        except Exception as e:
            print(f"[ERROR] {p}: {e}")

def test_finance_search():
    print("\nTesting Market/Search APIs...")
    providers = ["alphavantage", "finnhub", "tavily"]
    for p in providers:
        try:
            print(f"Testing {p}...")
            provider = provider_registry.get(p)
            res = provider.get_quote("AAPL")
            print(f"[OK] {p}: Success. Fetched data.")
        except Exception as e:
            print(f"[ERROR] {p}: {e}")

def main():
    test_llms()
    test_finance_search()

if __name__ == "__main__":
    main()
