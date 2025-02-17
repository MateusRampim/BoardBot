class Board:
    def __init__(self):
        print("Dummy Board iniciada - teste sem hardware")
    
    def lift_pen(self):
        print("Dummy: levantando a caneta")
    
    def press_pen(self):
        print("Dummy: pressionando a caneta")

    def go_to_center(self):
        print(f"Dummy: indo para o centro")
    
    def go_to(self, x, y):
        print(f"Dummy: indo para ({x}, {y})")
    
    def draw_line(self, x, y):
        print(f"Dummy: desenhando linha para ({x}, {y})")
