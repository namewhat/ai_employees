@echo off
echo Starting backend...
start cmd /k "cd backend && python run.py"
echo Starting frontend...
start cmd /k "cd frontend && npm run dev"
echo Both backend and frontend are now running.