#!/bin/bash
export DISCORD_TOKEN=your_token_here
pip install -r requirements.txt
python bot.py &
python admin_web.py
