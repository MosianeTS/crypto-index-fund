# Crypto Index Fund

A web application that allows users to create and manage cryptocurrency index funds using React for the frontend and FastAPI for the backend.

## Project Structure

```
├── backend/
│   ├── cryptoindexfund/      # Django project configuration
│   ├── db.sqlite3            # SQLite database file
│   ├── fastapi_app/          # FastAPI application│  
│   └── manage.py             # Django management script
├── frontend/
│   ├── crypto-fund/          # React application
│   │   ├── node_modules/     # Node.js dependencies
│   │   ├── package.json      # Node.js configuration
│   │   ├── package-lock.json # Node.js dependency lock file
│   │   ├── public/           # Static files
│   │   ├── README.md         # React app README
│   │   └── src/              # React source code
├── db.sqlite3                # Root database file
├── diagram.md                # Project architecture diagram
├── env/                      # Python virtual environment

```

## Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- npm 6 or higher

## Installation

### Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/MosianeTS/crypto-index-fund.git
   cd crypto-index-fund
   ```

2. Set up the Python virtual environment:
   ```bash
   python -m venv env
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     .\env\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source env/bin/activate
     ```

4. Install the backend dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

   If requirements.txt is not available, install the necessary packages:
   ```bash
   pip install fastapi uvicorn django sqlalchemy python-dotenv requests
   ```

5. Run database migrations:
   ```bash
   python manage.py migrate
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd ../frontend/crypto-fund
   ```

2. Install the frontend dependencies:
   ```bash
   npm install
   ```

## Running the Application

### Start the Backend Server

1. From the backend directory, run:
   ```bash
   # Start the FastAPI server
   cd fastapi_app
   uvicorn main:app --reload --port 8000
   ```

### Start the Frontend Server

1. From the frontend/crypto-fund directory, run:
   ```bash
   npm start
   ```

2. The React application will open in your browser at http://localhost:3000

## Project Diagrams

- **Architecture Diagram**: See `diagram.md` for a detailed system architecture overview.

## Features

- Create custom cryptocurrency index funds
- Track performance of index funds in real-time
- Automatic rebalancing of fund assets
- Historical performance analytics
- User account management