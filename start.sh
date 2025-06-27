#!/bin/bash
python admin_web.py &  # run Flask in background
python bot.py          # run bot in foreground
