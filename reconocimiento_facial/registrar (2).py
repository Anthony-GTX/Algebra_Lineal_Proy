import cv2
import face_recognition
import numpy as np

nombre = input("Nombre de la persona (sin espacios): ")
cam = cv2.VideoCapture(0)
print("Mira a la camara. Presiona ESPACIO para capturar, ESC para salir")

while True:
    ok, frame = cam.read()
    if not ok:
        print("No se pudo abrir la camara")
        break
    cv2.imshow("Registro", frame)
    tecla = cv2.waitKey(1)
    if tecla == 27:          # ESC
        break
    if tecla == 32:          # ESPACIO
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        vectores = face_recognition.face_encodings(rgb)
        if len(vectores) == 1:
            np.save(f"{nombre}.npy", vectores[0])
            print("Vector guardado en", f"{nombre}.npy")
            print("Primeros 5 numeros de tu vector:", vectores[0][:5])
            break
        print("Debe haber exactamente 1 rostro visible, intenta de nuevo")

cam.release()
cv2.destroyAllWindows()
