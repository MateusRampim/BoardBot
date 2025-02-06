import image_processing
import vectorization
import optimization
import gcode_generator
import simulation

print("Processando imagem...")
imagem_bin = image_processing.processar_imagem("example.png")
print("Imagem processada!")

print("Extraindo contornos...")
contornos = vectorization.obter_contornos(imagem_bin)
print(f"{len(contornos)} contornos extraídos!")

print("Otimizando caminho...")
contornos_otimizados = optimization.otimizar_caminho(contornos)
print("Caminho otimizado!")

print("Gerando G-Code...")
gcode = gcode_generator.gerar_gcode(contornos_otimizados)

print("Salvando G-Code em output.gcode...")
with open("output.gcode", "w") as f:
    f.write(gcode)
print("G-Code salvo!")

print("Exibindo simulação...")
simulation.visualizar_trajeto(contornos_otimizados)
print("Processo concluído!")
