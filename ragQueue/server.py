from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Query
from redis import Redis
from rq import Queue
from .queues.worker import process_query



app = FastAPI()
queue = Queue(connection=Redis(
    host="localhost",
    port="6379"
))

@app.get("/")
def root():

    return {"status": "Server is running"}


@app.post("/chat")

def chat(
        query: str = Query(..., description="The input query string"  )
):
    job = queue.enqueue(process_query, query)
    return{"status": "Query queued", "job_id": job.id}

@app.get("/job-status")
def get_result(
    job_id: str = Query(..., description="The job ID to fetch the result for")
):
    job = queue.fetch_job(job_id)
    if not job:
        return {"status": "Job not found"}
    return {
        "status": job.get_status(),
        "result": job.result if job.is_finished else None
    }