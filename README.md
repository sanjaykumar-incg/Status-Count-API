# Status-Count-API
Welcome to the Status Count API. This project shows how to simulate messages, process them, and store them in a database. It uses RabbitMQ to handle messages, MongoDB to store them, and FastAPI to provide a simple API that tells you how often each status appears within a given time range.

## What’s in This Project
This project has three main parts:
  1. client.py: A script that sends random status messages (between 0 and 6) to RabbitMQ every second.
  2. receive.py: This script takes the messages from RabbitMQ and saves them to MongoDB, adding a timestamp to each one.
  3. status_count_api.py: A FastAPI server that provides an API to count how many times each status appeared within a given time range.

## Prerequisites
Before running this project, make sure you have:
  1. Python 3.7+ installed on your machine.
  2. MongoDB and RabbitMQ running on your local machine or a server.
  3. You'll also need the following Python libraries:
      - pika
      - pymongo
      - fastapi
      - uvicorn
  4. To install the libraries run:
    `pip install -r requirements.txt`

## How to Clone the Repository and Get Started
### 1. Clone the Repository
To clone the repository to your local machine, follow these steps:
  1. Open a terminal (Command Prompt or Git Bash).
  2. Navigate to the directory where you want to save the project.
  3. Run the following command to clone the repository:
  ```
  git clone https://github.com/sanjaykumar-incg/Status-Count-API.git
  cd Status-Count-API
  ```

#### 2. Set Up RabbitMQ and MongoDB
  Make sure RabbitMQ and MongoDB are set up and running on your machine.

### 3. Run the Client
  Start the client by running this command: 
  ```
  python client.py
  ```
  This will start sending random status messages every second to RabbitMQ.

### 4. Run the Server
Next, run the `receive.py` script. This will listen for messages from RabbitMQ and save them to MongoDB:
```
python receive.py
```

### 5. Run the API
Now, run the FastAPI server to allow querying the status counts. Use this command:
```
python status_count_api.py
```
The server will be available at http://localhost:8000.

### 6. Use the API
You can use the following API endpoint to get the count of each status in a specific time range:
- GET /count_status?start=<start_time>&end=<end_time>: This will return the count of each status (0-6) that was received between the start and end time. Make sure the time is in this format: YYYY-MM-DD HH:MM:SS.
- Example request:
  ```
  http://localhost:8000/count_status?start=2024-12-07%10:55:32&end=2024-12-07%10:55:34
  ```
### 7. Example Response
The API will respond with a count of each status. For example:
```
{
  "status_counts": {
    "1": 1,
    "5": 1
  }
}
