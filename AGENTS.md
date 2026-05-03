# AGENTS.md - Interior AI Project

## Testing Commands

### Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Run Backend Server
```bash
cd backend
python app.py
```
Server runs on http://localhost:5000

### Run Frontend
Open `frontend/index.html` in a browser, or use a local server:
```bash
cd frontend
python -m http.server 8000
```
Then navigate to http://localhost:8000

### API Endpoints
- POST `/generate` - Generate room design
- GET `/outputs/` - Get generated images
- GET `/health` - Health check

### Environment Variables
Create `.env` file in backend:
```
OPENAI_API_KEY=your_api_key_here
```