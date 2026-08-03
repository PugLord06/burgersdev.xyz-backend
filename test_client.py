import sys
import json
import httpx

def run_test_client(url: str = "http://127.0.0.1:8000/chat", query: str = "What are Michael's top skills?") -> str:
    print(f"Connecting to {url} with query: '{query}'...")
    response_text = []
    
    with httpx.Client(timeout=30.0) as client:
        with client.stream("POST", url, json={"query": query}) as response:
            if response.status_code != 200:
                raise RuntimeError(f"HTTP request failed with status code {response.status_code}")
            
            for line in response.iter_lines():
                if line.startswith("data: "):
                    data_str = line[6:].strip()
                    try:
                        data_json = json.loads(data_str)
                        content = data_json.get("content", "")
                        response_text.append(content)
                        sys.stdout.write(content)
                        sys.stdout.flush()
                    except json.JSONDecodeError:
                        response_text.append(data_str)
                        sys.stdout.write(data_str)
                        sys.stdout.flush()
    print("\n--- Stream Finished ---")
    return "".join(response_text)

if __name__ == "__main__":
    query_input = sys.argv[1] if len(sys.argv) > 1 else "Tell me about Michael's education."
    full_resp = run_test_client(query=query_input)
    print(f"Total response length: {len(full_resp)} characters.")
