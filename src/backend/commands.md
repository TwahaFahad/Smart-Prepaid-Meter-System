# Local commands
python -m uvicorn core.asgi:application

uvicorn core.asgi:application --port 8000 --workers 4 --log-level debug --reload