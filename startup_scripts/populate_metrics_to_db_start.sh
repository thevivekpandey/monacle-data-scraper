#!/bin/bash
NAME="populate_to_db"
USER="ubuntu"
GROUP="ubuntu"

echo "starting $NAME"
exec python3 /home/ubuntu/engine/populate_metrics_to_db.py

