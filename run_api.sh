#!/bin/bash

# run app
uvicorn backend.main:app --reload --host 0.0.0.0 --port 5005
