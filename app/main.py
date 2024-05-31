from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.connect4 import Connect4

class DropPieceRequest(BaseModel):
    column: int

class GameStateResponse(BaseModel):
    board: List[List[int]]
    current_player: int
    winner: Optional[int]

app = FastAPI()
game = Connect4()

@app.post("/drop_piece", response_model=GameStateResponse)
def drop_piece(request: DropPieceRequest):
    if not game.drop_piece(request.column):
        raise HTTPException(status_code=400, detail="Invalid move")
    return GameStateResponse(board=game.board, current_player=game.current_player, winner=game.winner)

@app.get("/game_state", response_model=GameStateResponse)
def get_game_state():
    return GameStateResponse(board=game.board, current_player=game.current_player, winner=game.winner)
