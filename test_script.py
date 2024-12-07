import threading
import time
import requests
import pymongo
import pika
import json


# Test Configuration
mongo_uri = "mongodb://localhost:27017/"
mydb = "mqtt"
mycol = "status message"
api_endpoint = "http://127.0.0.1:8000/status_count"


def test_client():
    """
    Test the client.py script by simulating message publishing.
    """
    print("Starting client.py test...")
    def run_client():
        import client
        client.main()

    client_thread = threading.Thread(target=run_client, daemon=True)
    client_thread.start()

    time.sleep(5)
    client_thread.join(1)
    print("client.py test complete.")


def test_receive():
    """
    Test the receive.py script by consuming and verifying message insertion into MongoDB.
    """
    print("Starting receive.py test...")
    
    client = pymongo.MongoClient(mongo_uri)
    db = client[mydb]
    collection = db[mycol]
    collection.delete_many({}) 
    def run_receive():
        import receive
        receive.main()

    receive_thread = threading.Thread(target=run_receive, daemon=True)
    receive_thread.start()

    time.sleep(5)
    receive_thread.join(1)

    message_count = collection.count_documents({})
    assert message_count > 0, "No messages inserted into MongoDB!"
    print(f"Messages in MongoDB: {message_count}")
    print("receive.py test complete.")


def test_status_count_api():
    """
    Test the status_count_api.py script by verifying the API response.
    """
    print("Starting status_count_api.py test...")

    start_time = "2000-01-01 00:00:00"
    end_time = "3000-01-01 00:00:00"

    response = requests.get(api_endpoint, params={"start_time": start_time, "end_time": end_time})
    assert response.status_code == 200, f"API response failed with status code {response.status_code}"

    data = response.json()
    assert "status_counts" in data, "API response missing 'status_counts' key"
    print(f"API Response: {data}")
    print("status_count_api.py test complete.")


if __name__ == "__main__":
    print("Starting tests...")
    test_client()
    test_receive()
    test_status_count_api()
    
    print("All tests complete!")
