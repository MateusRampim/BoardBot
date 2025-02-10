if __name__=="__main__" and __package__ is None:
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    __package__ = "motor_controller"

import asyncio
import websockets
import json
import sys
if sys.platform == 'win32':
    from .dummy_board import Board  # Agora a importação relativa funcionará
else:
    from .board_controller import Board  # Alterado para importação relativa

async def process_gcode(websocket):
    board = Board()
    # Recebe o payload inicial contendo o G-Code
    data = await websocket.recv()
    try:
        payload = json.loads(data)
        gcode_str = payload.get("gcode", "")
        if not gcode_str:
            await websocket.send(json.dumps({"error": "Nenhum G-Code recebido"}))
            return
    except Exception as e:
        await websocket.send(json.dumps({"error": f"Erro na mensagem: {str(e)}"}))
        return

    # Cria um evento para sinalizar o cancelamento
    cancel_event = asyncio.Event()

    async def listen_cancel():
        try:
            async for message in websocket:
                msg = json.loads(message)
                if msg.get("cancel") is True:
                    cancel_event.set()
                    break
        except Exception as e:
            print(f"Erro no listener de cancelamento: {e}")

    cancel_task = asyncio.create_task(listen_cancel())

    gcode_lines = gcode_str.strip().splitlines()
    total_lines = len(gcode_lines)

    for i, line in enumerate(gcode_lines, start=1):
        if cancel_event.is_set():
            # Ao cancelar, levanta a caneta e move para (0,0)
            board.lift_pen()
            board.go_to(0, 0)
            await websocket.send(json.dumps({"status": "cancelado"}))
            cancel_task.cancel()
            return

        parts = line.strip().split()
        params = {"x": None, "y": None, "z": None}
        for part in parts[1:]:
            if part.startswith("X"):
                params["x"] = float(part[1:])
            elif part.startswith("Y"):
                params["y"] = float(part[1:])
            elif part.startswith("Z"):
                params["z"] = float(part[1:])

        if parts[0] == "G0":
            if params["x"] is not None and params["y"] is not None:
                board.go_to(params["x"], params["y"])
            elif params["z"] is not None:
                if params["z"] < 1:
                    board.press_pen()
                else:
                    board.lift_pen()
        elif parts[0] == "G1":
            if params["x"] is not None and params["y"] is not None:
                board.draw_line(params["x"], params["y"])

        progress = (i / total_lines) * 100
        await websocket.send(json.dumps({"progress": progress}))
        await asyncio.sleep(0.1)
    
    # Ao terminar, levanta a caneta e move para (0, 0) se necessário
    board.lift_pen()
    board.go_to(0, 0)
    await websocket.send(json.dumps({"status": "finalizado"}))
    cancel_task.cancel()

async def main():
    async with websockets.serve(process_gcode, "0.0.0.0", 8765):
        print("WebSocket G-Code server iniciado em ws://0.0.0.0:8765")
        await asyncio.Future()  

if __name__ == '__main__':
    asyncio.run(main())
