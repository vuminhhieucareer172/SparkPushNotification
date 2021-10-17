#!/bin/bash

# run migration mysql structure
cd backend && alembic upgrade head

# run app
cd .. && PYTHONPATH=$PWD python backend/main.py
