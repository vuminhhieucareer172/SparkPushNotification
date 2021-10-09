#!/bin/bash

# run migration mysql structure
cd backend && alembic upgrade head

# run app
cd .. && uvicorn backend.main:app --reload --host 0.0.0.0 --port 5005
