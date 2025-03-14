
# Balance Scale Addition Game

An interactive educational game that teaches addition through visual intuition using a balance scale interface. Students add numbers to match a target value, with immediate visual feedback through scale tilt.

## Features
- Interactive balance scale Game
- Real-time visual feedback
- Multiple difficulty levels
- Progress tracking
- Mobile-responsive design
- Admin interface for game configuration

## Tech Stack
### Frontend
- Vue.js 3
- TypeScript
- Vite
- Firebase Authentication
- Tailwind CSS
- Vue Router
- Pinia (State Management)
### Backend
- FastAPI
- Python
- Firebase/Firestore
- Pydantic
## Setup Instructions
### Prerequisites
- Node.js
- Python 3.6+
- npm/yarn
- Firebase account
### Installation
1. Clone the repo:
   ```sh
   git clone https://github.com/partiksingh1/hiring-challenge-build-in-public.git
   cd hiring-challenge-build-in-public
   ```

2. Frontend setup:
   ```sh
   cd frontend
   npm install
   npm run dev
   npm run build
   ```
3. Backend setup:
   ```sh
   cd backend
   python -m venv venv
   pip install -r requirements.txt
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

## Usage
### Student Interface
- Sign in using email/password or Google authentication
- Select Game
- Solve addition problems using the balance scale
- Receive immediate visual feedback
- Track progress
### Admin Interface
- Create new game
- Set difficulty
- Monitor student progress

## Licensing
This project is open source under the Apache License 2.0.