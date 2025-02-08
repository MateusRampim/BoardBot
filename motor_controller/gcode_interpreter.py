from board_controller import Board

import sys

if len(sys.argv) < 2:
    print("Usage: python gcode_interpreter.py <filename>")
    sys.exit(1)

filename = sys.argv[1]

board = Board()

def G0(x=None, y=None, z=None):
    if x is not None and y is not None:
        print(f'go to {x}, {y}')
        board.go_to(x, y)
    elif z is not None:
        if z < 1:
            print(f'press pen')
            board.press_pen()
        else:
            print(f'lift pen')
            board.lift_pen()

def G1(x=None, y=None, z=None):
    if x is not None and y is not None:
        print(f'draw line {x}, {y}')
        board.draw_line(x, y)

with open(filename, "r") as file:
    for line in file:
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
            G0(**params)
        elif parts[0] == "G1":
            G1(**params)
        elif parts[0] == "G21":
            print("Unidades em mm")
        elif parts[0] == "G90":
            print("Posição absoluta")
        else:
            raise Exception(f'gcode inválido: {parts[0]}')
