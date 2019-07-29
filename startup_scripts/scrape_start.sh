#!/bin/bash
NAME="scraper"
USER="ubuntu"
GROUP="ubuntu"

echo "starting $NAME"
exec python3 /home/ubuntu/engine/scrape.py

