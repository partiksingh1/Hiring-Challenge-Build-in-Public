import os
from fastapi import FastAPI, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from firebase_admin import auth, credentials, initialize_app
from google.cloud import firestore
import firebase_admin
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List

# Set the environment variable for Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./serviceAccountKey.json"

# Initialize Firebase Admin SDK
cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)

# Initialize Firestore Client
db = firestore.Client()

# FastAPI app initialization
app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS","DELETE"],
    allow_headers=["*"],
)

# Dependency to handle OAuth2 token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Pydantic models for request validation
class User(BaseModel):
    email: str
    password: str
    role: str

class GameConfig(BaseModel):
    id: Optional[str] = None
    gameName: str
    difficulty: str
    rounds: int

class UserProgress(BaseModel):
    user_id: str
    game_name: str
    score: int
    game_id: str
    email: Optional[str] = None 

class GameResponse(BaseModel):
    message: str
    id: str

class LoginResponse(BaseModel):
    id_token: str
    user_id: str
    role: str
    message: str

# ---- HELPER FUNCTION ----
def verify_firebase_token(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Firebase Token")

# ---- API ROUTES ----

@app.post("/signup")
async def register_user(data: dict):
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")  # "admin" or "user"

    if not email or not password or role not in ["admin", "user"]:
        raise HTTPException(status_code=400, detail="Invalid input")

    # Create user in Firebase Auth
    user = auth.create_user(email=email, password=password)

    # Store role in Firestore
    db.collection("users").document(user.uid).set({"email": email, "role": role})

    return {"message": "User registered successfully", "uid": user.uid, "role": role}

@app.post("/login")
async def login_user(request: Request, response: Response):
    body = await request.json()
    id_token = body.get("id_token")

    if not id_token:
        raise HTTPException(status_code=400, detail="ID token required")

    user_data = verify_firebase_token(id_token)
    uid = user_data["uid"]

    # Fetch user role from Firestore
    user_doc = db.collection("users").document(uid).get()
    if not user_doc.exists:
        raise HTTPException(status_code=404, detail="User not found")

    role = user_doc.to_dict()["role"]

    # Set session cookie
    response.set_cookie(
        key="session_token",
        value=id_token,
        httponly=True,
        secure=True,
        samesite="Lax",
    )

    return {"message": "Login successful", "role": role}

@app.get("/check-session")
async def check_session(request: Request):
    session_token = request.cookies.get("session_token")
    if not session_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    user_data = verify_firebase_token(session_token)
    uid = user_data["uid"]

    user_doc = db.collection("users").document(uid).get()
    if not user_doc.exists:
        raise HTTPException(status_code=404, detail="User not found")

    role = user_doc.to_dict()["role"]
    return {"role": role}

@app.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("session_token")
    decoded_token = verify_token(token)
    user_ref = db.collection("users").document(decoded_token['uid'])
    user_doc = user_ref.get()
    if user_doc.exists:
        return User(**user_doc.to_dict())
    else:
        raise HTTPException(status_code=404, detail="User not found")

# Route to set game configuration
@app.post("/game/configure", response_model=GameResponse)
async def configure_game(game_config: GameConfig):
    # Create a new document reference with an auto-generated ID
    game_ref = db.collection("game_configs").document()  # Create a new document reference
    game_ref.set(game_config.dict())  # Set the data for the new document
    
    # Return the generated ID in the response
    return GameResponse(message="Game configuration saved successfully!", id=game_ref.id)

# Route to get all game configurations
@app.get("/game/configure", response_model=list[GameConfig])
async def get_all_game_configs():
    game_configs_ref = db.collection("game_configs")
    game_configs_docs = game_configs_ref.stream()

    all_game_configs = []
    for game_config_doc in game_configs_docs:
        # Create a dictionary from the document data
        game_config_data = game_config_doc.to_dict()

        # Remove 'id' from game_config_data if it's present, since we'll add it manually
        game_config_data.pop('id', None)  # Avoid key error if 'id' is not in data

        # Create a GameConfig instance, including the document ID
        game_config = GameConfig(id=game_config_doc.id, **game_config_data)
        all_game_configs.append(game_config)

    return all_game_configs

# Route to delete a game configuration
@app.delete("/game/configure/{game_id}", response_model=GameResponse)
async def delete_game_config(game_id: str):
    game_ref = db.collection("game_configs").document(game_id)
    game_ref.delete()  # Delete the document
    return GameResponse(message="Game configuration deleted successfully!", id=game_id)

@app.get("/game/configure/{game_id}", response_model=GameConfig)
async def get_game_config_by_id(game_id: str):
    # Reference to the specific game configuration document by ID
    game_ref = db.collection("game_configs").document(game_id)
    game_doc = game_ref.get()  # Get the document

    if not game_doc.exists:
        raise HTTPException(status_code=404, detail="Game configuration not found")

    # Convert document data to a dictionary
    game_config_data = game_doc.to_dict()
    
    # Ensure that 'id' is removed from game_config_data before passing it to GameConfig
    game_config_data.pop('id', None)  # This ensures the 'id' field is removed from the data

    # Create a GameConfig instance with the document ID and the rest of the data
    game_config = GameConfig(id=game_doc.id, **game_config_data)

    return game_config

    # Check if the user exists in Firestore
    user_ref = db.collection("users").document(user_progress.user_id)
    user_doc = user_ref.get()

    if not user_doc.exists:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if the game configuration exists in Firestore
    game_ref = db.collection("game_configs").document(user_progress.game_id)
    game_doc = game_ref.get()

    if not game_doc.exists:
        raise HTTPException(status_code=404, detail="Game configuration not found")

    # Store user progress in Firestore under user progress sub-collection (not overwriting)
    progress_ref = db.collection("users").document(user_progress.user_id).collection("progress").document()  # Automatically create a new document
    progress_ref.set(user_progress.dict())  # Save new progress entry

    return GameResponse(message="Progress saved successfully!", id=progress_ref.id)

# Route to get all user progress by user_id (using userId in the URL)
@app.get("/game/progress/{user_id}", response_model=list[UserProgress])
async def get_user_progress(user_id: str):
    # Check if the user exists in Firestore
    user_ref = db.collection("users").document(user_id)
    user_doc = user_ref.get()

    if not user_doc.exists:
        raise HTTPException(status_code=404, detail="User not found")

    # Retrieve all user progress from Firestore (from the 'progress' sub-collection)
    progress_ref = db.collection("users").document(user_id).collection("progress")
    progress_docs = progress_ref.stream()

    # Convert each document into a UserProgress model
    all_progress = []
    for progress_doc in progress_docs:
        progress_data = progress_doc.to_dict()
        game_id = progress_data.get("game_id")

        if game_id:
            # Fetch game config for the given game_id
            game_ref = db.collection("game_configs").document(game_id)
            game_doc = game_ref.get()

            if game_doc.exists:
                game_data = game_doc.to_dict()
                # Add game_name to progress data
                progress_data["game_name"] = game_data.get("gameName")
            else:
                # If the game config doesn't exist, raise an error
                raise HTTPException(status_code=404, detail=f"Game configuration with id {game_id} not found.")

        # Create a UserProgress instance with the game_name field populated
        all_progress.append(UserProgress(**progress_data))

    if all_progress:
        return all_progress
    else:
        raise HTTPException(status_code=404, detail="No progress found for the user")

@app.get("/game/users/progress", response_model=list[UserProgress])
async def get_all_user_progress():
    # Retrieve all user progress from Firestore using collection_group
    progress_ref = db.collection_group("progress")  # Fetch progress from all users
    progress_docs = progress_ref.stream()

    # Convert the documents to a list of UserProgress models
    all_progress = []
    for progress_doc in progress_docs:
        progress_data = progress_doc.to_dict()

        # Fetch the game_name from the game_configs collection using game_id
        game_id = progress_data.get("game_id")
        if game_id:
            game_ref = db.collection("game_configs").document(game_id)
            game_doc = game_ref.get()

            if game_doc.exists:
                game_data = game_doc.to_dict()
                progress_data["game_name"] = game_data.get("gameName")  # Add the game_name to progress data
            else:
                # Handle case where the game config doesn't exist
                progress_data["game_name"] = "Unknown Game"
                        # Fetch the user's email using user_id
        user_id = progress_data.get("user_id")
        if user_id:
            user_ref = db.collection("users").document(user_id)
            user_doc = user_ref.get()

            if user_doc.exists:
                user_data = user_doc.to_dict()
                progress_data["email"] = user_data.get("email")  # Add the user's email to progress data
            else:
                progress_data["email"] = "Unknown User"  # Handle case where user doesn't exist

        # Create a UserProgress instance with the game_name field populated
        all_progress.append(UserProgress(**progress_data))

    return all_progress

# Route to get all scores of a user by user_id
@app.get("/game/scores/{user_id}", response_model=list[UserProgress])
async def get_all_scores(user_id: str):
    # Check if the user exists in Firestore
    user_ref = db.collection("users").document(user_id)
    user_doc = user_ref.get()

    if not user_doc.exists:
        raise HTTPException(status_code=404, detail="User not found")

    # Retrieve all scores (progress) for the user from the user's 'progress' sub-collection
    progress_ref = db.collection("users").document(user_id).collection("progress")
    progress_docs = progress_ref.stream()

    # Convert the documents to a list of UserProgress models
    all_scores = []
    for progress_doc in progress_docs:
        progress_data = progress_doc.to_dict()
        
        # Optionally, fetch the game_name from the game_configs collection if not in the progress
        game_id = progress_data.get("game_id")
        if game_id:
            game_ref = db.collection("game_configs").document(game_id)
            game_doc = game_ref.get()

            if game_doc.exists:
                game_data = game_doc.to_dict()
                progress_data["game_name"] = game_data.get("gameName")  # Add the game_name to progress data
            else:
                # Handle case where the game config doesn't exist
                progress_data["game_name"] = "Unknown Game"
        
        # Create a UserProgress instance with the game_name field populated
        all_scores.append(UserProgress(**progress_data))

    if all_scores:
        return all_scores
    else:
        raise HTTPException(status_code=404, detail="No scores found for the user")
