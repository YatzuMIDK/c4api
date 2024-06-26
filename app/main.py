from typing import List, Optional, Dict
from fastapi import FastAPI, HTTPException
from datetime import datetime
from pydantic import BaseModel
import uuid
from app.connect4 import Connect4

class CreateGameResponse(BaseModel):
    game_id: str

class DropPieceRequest(BaseModel):
    player: int
    column: int

class GameStateResponse(BaseModel):
    board: str
    current_player: int
    winner: Optional[int]

app = FastAPI()
games: Dict[str, Connect4] = {}
start_time = datetime.now()
# Función para obtener detalles de tiempo de actividad y ping
def get_server_details():
    # Calcular el tiempo de actividad
    uptime = datetime.now() - start_time
    uptime_str = str(uptime).split('.')[0]
    
    
    return {"uptime": uptime_str}

@app.get("/")
def root():
    return get_server_details()

@app.post("/crear", response_model=CreateGameResponse)
def create_game():
    game_id = str(uuid.uuid4())
    games[game_id] = Connect4()
    return CreateGameResponse(game_id=game_id)

@app.post("/drop/{game_id}", response_model=GameStateResponse)
def drop_piece(game_id: str, request: DropPieceRequest):
    game = games.get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    if game.winner:
        raise HTTPException(status_code=400, detail="The game has already been won.")
    
    if game.current_player != request.player:
        raise HTTPException(status_code=400, detail="It is not the turn of this player.")
    
    if not game.drop_piece(request.column):
        raise HTTPException(status_code=400, detail="Invalid move")
    
    return GameStateResponse(board=game.get_board_with_emojis(), current_player=game.current_player, winner=game.winner)

@app.get("/game_state/{game_id}", response_model=GameStateResponse)
def get_game_state(game_id: str):
    game = games.get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return GameStateResponse(board=game.get_board_with_emojis(), current_player=game.current_player, winner=game.winner)
