from event_handlers import search_for_dungeon, explore_dungeon
from character import Party, Profession
from choice_handlers import party_selector
# TODO: Handle Printing

if __name__ == "__main__":
    profession: Profession = party_selector()
    player_party: Party = Party(profession)
    output_stream = TerminalInterface()
    game = Game(player_party)
    game.start(output_stream)
    print(f"Your Score: {player_party.treasure}")


# app = FastAPI()
# @app.post("/api/action")
# async def perform_action(action: str):
#     profession: Profession = party_selector()
#     player_party: Party = Party(profession)
#     output_stream = TerminalInterface()
#     game = Game(player_party)
#     game.start(output_stream)
#
#     output = "\n".join(game.get_output())  # get output from TerminalInterface
#     return {"output_stream": output}
#
#
# async def process_data(websocket: WebSocket):
#     while True:
#         try:
#             data = await websocket.receive_text()
#             output = await perform_action(data)
#             await websocket.send_text(output['output_stream'])  # send output back to frontend through WebSocket
#         except WebSocketDisconnect:
#             break
#
#
# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     await process_data(websocket)
