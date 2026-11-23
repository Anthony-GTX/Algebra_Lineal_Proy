import cv2
import face_recognition
import numpy as np
import glob, os, time
from matematica import (M, CLAVE, CLAVE_INV, cifrar, descifrar, determinante,
                        adjunta, producto, distancia_euclidiana, similitud_coseno)

UMBRAL = 0.5   # distancia maxima para aceptar un rostro


# ---------- LOGIN FACIAL ----------
def login_facial(tiempo_max=15, aciertos_necesarios=5):
    conocidos, nombres = [], []
    for archivo in glob.glob("*.npy"):
        conocidos.append(np.load(archivo))
        nombres.append(os.path.splitext(archivo)[0])
    if not conocidos:
        print("No hay rostros registrados. Ejecuta registrar.py primero.")
        return None

    cam = cv2.VideoCapture(0)
    inicio = time.time()
    aciertos, ultimo = 0, None

    while time.time() - inicio < tiempo_max:
        ok, frame = cam.read()
        if not ok:
            break
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        ubicaciones = face_recognition.face_locations(rgb)
        vectores = face_recognition.face_encodings(rgb, ubicaciones)
        texto = "Buscando rostro..."

        for v in vectores:
            # distancia euclidiana (calculada por nosotros) contra cada rostro registrado
            distancias = [distancia_euclidiana(c, v) for c in conocidos]
            i = int(np.argmin(distancias))
            coseno = similitud_coseno(conocidos[i], v)
            if distancias[i] < UMBRAL:
                if nombres[i] == ultimo:
                    aciertos += 1
                else:
                    ultimo, aciertos = nombres[i], 1
                texto = (f"{nombres[i]} d={distancias[i]:.3f} cos={coseno:.3f} "
                         f"({aciertos}/{aciertos_necesarios})")
            else:
                texto = f"Desconocido d={distancias[i]:.3f} cos={coseno:.3f}"

        cv2.putText(frame, texto, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("Login facial", frame)
        cv2.waitKey(1)

        if aciertos >= aciertos_necesarios:
            cam.release()
            cv2.destroyAllWindows()
            return ultimo

    cam.release()
    cv2.destroyAllWindows()
    return None


# ---------- APP ----------
def mostrar_clave():
    print("\nMatriz clave K:")
    for fila in CLAVE:
        print("  ", fila)
    det = determinante(CLAVE)
    print(f"\ndet(K) = {det}   ->   det(K) mod {M} = {det % M}")
    print("\nAdjunta de K (transpuesta de la matriz de cofactores):")
    for fila in adjunta(CLAVE):
        print("  ", fila)
    print(f"\nInversa K^-1 = det^-1 * adj(K) (mod {M}):")
    for fila in CLAVE_INV:
        print("  ", fila)
    print(f"\nComprobacion K x K^-1 (mod {M}), debe ser la identidad:")
    for fila in producto(CLAVE, CLAVE_INV):
        print("  ", [x % M for x in fila])


def menu(usuario):
    while True:
        print(f"\n=== Bienvenido, {usuario} ===")
        print("1. Enviar mensaje cifrado")
        print("2. Leer mensajes de un archivo")
        print("3. Descifrar numeros recibidos")
        print("4. Ver matriz clave e inversa")
        print("5. Salir")
        op = input("Opcion: ")

        if op == "1":
            msg = input("Mensaje (sin tildes ni numeros): ")
            c = cifrar(msg)
            print("\nNumeros cifrados (copialos y envialos):")
            print(c)
            with open("mensajes.txt", "a", encoding="utf-8") as f:
                f.write(f"{usuario}|{c}\n")

        elif op == "2":
            archivo = input("Archivo (Enter = mensajes.txt): ") or "mensajes.txt"
            if not os.path.exists(archivo):
                print("No existe ese archivo.")
                continue
            with open(archivo, encoding="utf-8") as f:
                for linea in f:
                    if "|" not in linea:
                        continue
                    remitente, c = linea.rstrip("\n").split("|", 1)
                    print(f"{remitente}: {descifrar(c)}   (cifrado: {c})")

        elif op == "3":
            c = input("Pega aqui los numeros recibidos: ")
            print("Mensaje:", descifrar(c))

        elif op == "4":
            mostrar_clave()

        elif op == "5":
            break


if __name__ == "__main__":
    print("Mira a la camara para iniciar sesion...")
    usuario = login_facial()
    if usuario:
        menu(usuario)
    else:
        print("Acceso denegado.")
