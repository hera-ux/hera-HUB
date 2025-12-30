import subprocess

def sherlock():
    texto = input("Nombres a buscar: ")
    nombres = texto.split()

    for nombre in nombres:
        subprocess.run(["sherlock", nombre])

sherlock()
input("enter para salir")
