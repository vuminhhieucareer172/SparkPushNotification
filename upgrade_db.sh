#!/bin/bash

# run migration mysql structure
cd backend && alembic upgrade head

cd ..
