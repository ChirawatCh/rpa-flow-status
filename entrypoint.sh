#!/bin/bash

# Run your Python import script
python database/create_table.py
python database/import_data_v2.py

# Start the FastAPI application using uvicorn
uvicorn src.main:app --host 0.0.0.0 --port 80 --reload
