import os 
import random 

mayusculas = ["A","B","C","D","E","F","G","H","I","J","K","L","M",
              "N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
minusculas = ["a","b","c","d","e","f","g","h","i","j","k","l","m",
              "n","o","p","q","r","s","t","u","v","w","x","y","z"]
digitos = ["0","1","2","3","4","5","6","7","8","9"]
especiales = ["!", "\"", "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-",
              ".", "/", ":", ";", "<", "=", ">", "?", "@", "[", "\\", "]",
              "^", "_", "`", "{", "|", "}", "~"]

print("¿Qué nivel de seguridad deseas?")
print("1 - Solo minúsculas")
print("2 - Minúsculas y mayúsculas")
print("3 - Minúsculas, mayúsculas y dígitos")
print("4 - Todo (minúsculas, mayúsculas, dígitos y caracteres especiales)")
nivel = int(input("Selecciona (1-4): "))

print("¿De cuántos dígitos la quieres?")
longitud = int(input("Ingresa 8, 16, 24 o cualquier número: "))

print("¿Cuántas contraseñas necesitas?")
cantidad = int(input("Cantidad: "))

def generar(nivel, longitud, cantidad):
    # Seleccionar caracteres según el nivel
    if nivel == 1:
        caracteres = minusculas
    elif nivel == 2:
        caracteres = minusculas + mayusculas
    elif nivel == 3:
        caracteres = minusculas + mayusculas + digitos
    elif nivel == 4:
        caracteres = minusculas + mayusculas + digitos + especiales
    else:
        print("Nivel inválido")
        return
    
    # Generar las contraseñas y guardar en archivo
    with open("contraseñas.txt", "w") as archivo:
        for i in range(cantidad):
            contraseña = ""
            for j in range(longitud):
                contraseña += random.choice(caracteres)
            print(f"Contraseña {i+1}: {contraseña}")
            archivo.write(contraseña + "\n")
    
    print("\n✓ Contraseñas guardadas en 'contraseñas.txt'")

# Llamar a la función
generar(nivel, longitud, cantidad)
input("\nPresiona enter para cerrar...")
