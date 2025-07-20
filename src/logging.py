import sys
from pathlib import Path

config = {
    'handlers': [
        {'sink': sys.stdout, 'level': 'INFO', 'colorize': True, 'format':"<green>{time}</green> | <blue>{level}</blue> | <level>{message}</level>"},
        {'sink': Path(__file__).parent.parent / 'logs' / 'app.log', 'level': 'DEBUG', 'rotation': '1 MB', 'compression': 'zip', 'format': '{time} | {level} | {message}'},
        {'sink': Path(__file__).parent.parent / 'logs' / 'error.log', 'level': 'ERROR', 'rotation': '1 MB', 'compression': 'zip', 'format': '{time} | {level} | {message}'}
    ]
}