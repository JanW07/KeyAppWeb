#!/bin/bash
python -m pip install --upgrade pip
pip install -r /app/requirements.txt
cd /app
python /app/main.py
