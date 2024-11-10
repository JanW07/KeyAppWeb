#!/bin/bash
python -m pip install --upgrade pip
cd /app
pip install -r requirements.txt
python main.py
