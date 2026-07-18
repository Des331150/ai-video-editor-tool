# Python + React + Postgres Stack

**Backend**: Python. **Frontend**: React + Vite SPA. **AI**: Python in-process (same service). **Database**: Postgres. **Deployment**: Single Python service + Postgres.

Initially considered Go for the API server with a separate Python AI microservice, but the operational complexity of managing two runtimes doesn't justify the performance gains for a solo-creator MVP. Python's AI/ML ecosystem (Whisper, LLM clients, audio processing) means all AI capabilities run in-process, eliminating network hops between services. Python's asyncio and background task patterns (Celery, ARQ, or FastAPI's BackgroundTasks) are sufficient for the concurrency needs of this stage.

If the product scales to many concurrent users or requires real-time collaboration features, a future migration to Go for the API layer can be evaluated against the migration cost.
