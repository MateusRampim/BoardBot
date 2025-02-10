import subprocess

p1 = subprocess.Popen(["python", "router/websocket_server.py"])
p2 = subprocess.Popen(["python", "motor_controller/gcode_websocket.py"])

p1.wait()
p2.wait()
