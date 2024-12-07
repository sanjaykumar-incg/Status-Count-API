import pymongo
from fastapi import FastAPI, Query


# Initialize MongoDB client and define database and collection
myclient = pymongo.MongoClient("mongodb://localhost:27017/")    
mydb = myclient["mqtt"]
mycol = mydb["status message"]


# Initialize FastAPI app
app = FastAPI()


@app.get('/status_count')
async def status_count(start_time: str=Query(), end_time: str=Query()):
    """
    API endpoint to count the occurrences of each status within a specified time range.
    """
    pipeline = [
        {"$match": {"timestamp": {"$gte": start_time, "$lte": end_time}}},
    ]
    results = list(mycol.aggregate(pipeline))
    grouped_data = {'status_counts': {}}
    for result in results:
        if result['status'] not in grouped_data['status_counts']:
            grouped_data['status_counts'][result['status']] = 1
        else:
            grouped_data['status_counts'][result['status']] += 1
    return grouped_data


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)