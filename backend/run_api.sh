#!/bin/bash

# run app
uvicorn main:app --reload --host 0.0.0.0 --port 5005
