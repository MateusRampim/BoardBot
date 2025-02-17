import sys
if sys.platform == 'win32':
    from .dummy_board import Board  # Importa o dummy para Windows
else:
    from .board_controller import Board  # Importa o board controller fora do rasp

def main():
    board = Board()
    # Define pontos incluindo extremos e pontos intermediários
    points = [
        (0, 0),
        (100, 0),
        (200, 0),
        (200, 100),
        (200, 200),
        (100, 200),
        (0, 200),
        (0, 100),
        (0, 0)
    ]
    
    # Rotina com caneta levantada
    print("Board Tester iniciado com a caneta levantada.")
    board.lift_pen()  # Garante que a caneta esteja levantada
    print("Rotina com caneta levantada iniciada. Pressione Enter para ir ao próximo ponto.")
    for point in points:
        input(f"Pressione Enter para mover para {point}...")
        board.go_to(*point)
        print(f"Movendo para {point}...")
    
    print("Teste finalizado com a caneta levantada.")
    
    # Rotina com a caneta baixada
    print("\nIniciando teste com a caneta baixada.")
    board.press_pen()  # Baixa a caneta
    print("Rotina com caneta baixada iniciada. Pressione Enter para desenhar para o próximo ponto.")
    for point in points:
        input(f"Pressione Enter para desenhar para {point}...")
        board.draw_line(*point)
        print(f"Desenhando para {point}...")
    
    # Finaliza levantando a caneta e retornando para (0, 0)
    board.lift_pen()
    board.go_to(0, 0)
    print("Teste finalizado com caneta baixada. Caneta levantada e retornada para (0,0).")

if __name__ == "__main__":
    main()
