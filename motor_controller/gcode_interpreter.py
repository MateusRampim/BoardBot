from board_controller import Board

import sys

if len(sys.argv) < 2:
    print("Usage: python gcode_interpreter.py <filename>")
    sys.exit(1)

filename = sys.argv[1]

board = Board()

def G0(x=None, y=None, z=None):
    if x is not None and y is not None:
        board.go_to(x, y)
        print(f'go to {x}, {y}')
    elif z is not None:
        if z < 1:
            board.press_pen()
            print(f'press pen')
        else:
            board.lift_pen()
            print(f'lift pen')

with open(filename, "r") as file:
    for line in file:
        parts = line.strip().split()

        if parts[0] == "G0":
            params = {"x": None, "y": None, "z": None}
            for part in parts[1:]:
                if part.startswith("X"):
                    params["x"] = float(part[1:])
                elif part.startswith("Y"):
                    params["y"] = float(part[1:])
                elif part.startswith("Z"):
                    params["z"] = float(part[1:])
            G0(**params)
