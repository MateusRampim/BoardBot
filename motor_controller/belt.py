from RpiMotorLib import RpiMotorLib

class Belt:
    def __init__(self, step, dir):
        # Steps/mm: 5 = Steps/cm: 50
        self.tamanho_passo = 0.02 # cm
        self.pos = 0
        self.motor = RpiMotorLib.A4988Nema(dir, step, (-1, -1, -1), "DRV8825")

    def go_to(self, pos):
        delta_passos = int((pos - self.pos)/self.tamanho_passo)
        n_passos = abs(delta_passos)
        dir = delta_passos > 0

        print(f'pos={pos} self.pos={self.pos} delta={delta_passos} n_passos={n_passos} dir={dir}')

        self.motor.motor_go(clockwise=dir, steptype="Full", steps=n_passos, stepdelay=.001, verbose=True, initdelay=.0)
        self.pos += delta_passos * self.tamanho_passo
