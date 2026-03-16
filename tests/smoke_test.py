import requests
import time

BASE_URL = "http://127.0.0.1:8000/v1/video"
YOUTUBE_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Example URL


def run_test():
    # 1. Ingest Video
    print("--- Testing Ingest ---")
    payload = {"url": YOUTUBE_URL, "depth": "standard"}
    response = requests.post(f"{BASE_URL}/ingest", json=payload)

    if response.status_code != 202:
        print(f"FAILED: Expected 202, got {response.status_code}")
        print(response.json())
        return

    data = response.json()
    task_id = data["video_processing_task_id"]
    print(f"SUCCESS: Created task {task_id}")

    # 2. Check Status
    print("\n--- Testing Status ---")
    status_response = requests.get(f"{BASE_URL}/status/{task_id}")

    if status_response.status_code == 200:
        print("SUCCESS: Data retrieved from database!")
        print(status_response.json())
    else:
        print(f"FAILED: Could not find task in DB. Status: {status_response.status_code}")


if __name__ == "__main__":
    run_test()