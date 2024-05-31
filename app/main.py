from typing import List, Optional, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
from app.connect4 import Connect4

class CreateGameResponse(BaseModel):
    game_id: str

class DropPieceRequest(BaseModel):
    column: int

class GameStateResponse(BaseModel):
    board: List[List[int]]
    current_player: int
    winner: Optional[int]

app = FastAPI()
games: Dict[str, Connect4] = {}

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
    if not game.drop_piece(request.column):
        raise HTTPException(status_code=400, detail="Invalid move")
    return GameStateResponse(board=game.board, current_player=game.current_player, winner=game.winner)

@app.get("/game/{game_id}", response_model=GameStateResponse)
def get_game_state(game_id: str):
    game = games.get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return GameStateResponse(board=game.board, current_player=game.current_player, winner=game.winner)
