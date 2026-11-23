import cv2
import face_recognition
import numpy as np

nombre = input("Nombre de la persona (sin espacios): ")
cam = cv2.VideoCapture(0)
print("Mira a la camara. ESPACIO = capturar, ESC = salir")

while True:
    ok, frame = cam.read()
    if not ok:
        print("No se pudo abrir la camara")
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 1) Detectar donde esta el rostro: (arriba, derecha, abajo, izquierda) en pixeles
    ubicaciones = face_recognition.face_locations(rgb)
    # 2) Encontrar los 68 puntos de referencia (ojos, cejas, nariz, boca, mandibula)
    puntos_cara = face_recognition.face_landmarks(rgb, ubicaciones)

    vista = frame.copy()
    for (arriba, derecha, abajo, izquierda) in ubicaciones:
        cv2.rectangle(vista, (izquierda, arriba), (derecha, abajo), (0, 255, 0), 2)
    for rostro in puntos_cara:
        for parte, puntos in rostro.items():
            for (x, y) in puntos:
                cv2.circle(vista, (x, y), 2, (0, 255, 255), -1)

    if len(ubicaciones) == 1:
        mensaje, color = "1 rostro detectado - ESPACIO para guardar", (0, 255, 0)
    elif len(ubicaciones) == 0:
        mensaje, color = "No se detecta rostro", (0, 0, 255)
    else:
        mensaje, color = "Hay mas de un rostro", (0, 165, 255)
    cv2.putText(vista, mensaje, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    cv2.imshow("Registro", vista)

    tecla = cv2.waitKey(1)
    if tecla == 27:              # ESC
        break
    if tecla == 32:              # ESPACIO
        if len(ubicaciones) == 1:
            # 3) Convertir el rostro en el vector de 128 numeros
            vector = face_recognition.face_encodings(rgb, ubicaciones)[0]
            np.save(f"{nombre}.npy", vector)
            print("Vector guardado en", f"{nombre}.npy")
            print("Coordenadas del rostro (arriba, derecha, abajo, izquierda):", ubicaciones[0])
            print("Puntos de referencia detectados:", sum(len(p) for p in puntos_cara[0].values()))
            print("Cantidad de numeros del vector:", len(vector))
            print("Primeros 5 numeros del vector:", vector[:5])
            break
        print("Debe haber exactamente 1 rostro visible, intenta de nuevo")

cam.release()
cv2.destroyAllWindows()