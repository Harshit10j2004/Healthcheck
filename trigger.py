import requests
import schedule
import time
import logging
import os
from dotenv import load_dotenv

load_dotenv(os.getenv("DOTENV_PATH", "healthcheck.env"))
log_path = os.getenv("LOG_PATH", "logs/logs.txt")
log_dir = os.path.dirname(log_path)

if not os.path.exists(log_dir):
    os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level= logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename = log_path,
    filemode='a'
)

def call_handeling():
    try:
        response = requests.post("http://handelingapi:8002/handeling")
        print(f"[INFO] Status: {response.status_code} | Response: {response.json()}")
    except Exception as e:

        logging.error(f"Error occured during sending request to handling service from trigger {e}")
        print("issue", e)

# Schedule the task every 30 seconds
schedule.every(30).seconds.do(call_handeling)

print("[INFO] Starting automated health checks every 30 sec...")
while True:
    schedule.run_pending()
    time.sleep(1)

