def gerar_gcode(contornos):
    gcode = ["G21 ; Unidades em mm", "G90 ; Posição absoluta", "G0 Z5 ; Levantar caneta"]

    for c in contornos:
        pontos = c.reshape(-1, 2)
        x, y = pontos[0]
        gcode.append(f"G0 X{x:.2f} Y{y:.2f}")  # Mover para o início do traço
        gcode.append("G0 Z0 ; Abaixar caneta")

        for x, y in pontos[1:]:
            gcode.append(f"G1 X{x:.2f} Y{y:.2f}")  # Desenhar

        gcode.append("G0 Z5 ; Levantar caneta")  # Levantar caneta ao final do traço

    return "\n".join(gcode)
