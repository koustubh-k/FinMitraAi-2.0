import os
import json
import time
from dotenv import load_dotenv

import sys

# Load env before importing app modules
api_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
project_root = os.path.dirname(os.path.dirname(api_path))
sys.path.append(api_path)
env_path = os.path.join(project_root, '.env')
load_dotenv(env_path)

from app.agents.supervisor import route_query
from app.agents.state import AssistantState
from app.core.logger import setup_logger

logger = setup_logger(__name__)

def evaluate_routing(dataset_path: str):
    logger.info(f"Starting routing evaluation with {dataset_path}")
    
    total = 0
    passed = 0
    failed = []
    
    with open(dataset_path, "r") as f:
        for line in f:
            if not line.strip():
                continue
                
            data = json.loads(line)
            query = data["query"]
            expected = data["expected_route"]
            
            state: AssistantState = {
                "query": query,
                "status": "started",
                "route": "",
                "user_id": "eval_user",
                "chat_history": []
            }
            
            start_time = time.perf_counter()
            result_state = route_query(state)
            duration_ms = (time.perf_counter() - start_time) * 1000
            
            actual = result_state.get("route")
            
            total += 1
            if actual == expected:
                passed += 1
                logger.info(f"PASS | {expected} | {query[:40]}... ({duration_ms:.2f}ms)")
            else:
                logger.error(f"FAIL | Expected: {expected}, Got: {actual} | {query}")
                failed.append({
                    "query": query,
                    "expected": expected,
                    "actual": actual
                })
                
    accuracy = (passed / total) * 100 if total > 0 else 0
    logger.info(f"Routing Evaluation Complete. Accuracy: {accuracy:.2f}% ({passed}/{total})")
    
    return {
        "total": total,
        "passed": passed,
        "accuracy": accuracy,
        "failed_cases": failed
    }

if __name__ == "__main__":
    dataset_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "datasets", "routing.jsonl")
    evaluate_routing(dataset_file)
