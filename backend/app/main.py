"""
main.py
-------
This is the entrypoint of our backend. Running this file starts the
FastAPI server that your React frontend will talk to.

To run (from the backend/ folder, with venv activated):
    uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base
from .routes import products

# This line creates all tables (matched_product, raw_listing, price_history)
# in Postgres automatically, based on models.py -- no manual SQL needed
# once this runs.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Shopping Comparison API")

# CORS lets our React frontend (running on a different port) call this API.
# In production you'd restrict this to your actual frontend domain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router)


@app.get("/")
def root():
    return {"message": "Shopping Comparison API is running"}
