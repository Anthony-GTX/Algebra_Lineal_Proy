"""
pruebas.py - Casos de prueba del proyecto (no usa camara).
Compara lo esperado (calculado a mano o con sympy) contra lo obtenido por nuestro codigo.
Ejecutar con:  python pruebas.py
"""
import numpy as np
from sympy import Matrix
from matematica import (CLAVE, M, N, cifrar, descifrar, a_numeros, inversa_modular,
                        producto, distancia_euclidiana, similitud_coseno)

resultados = []


def verificar(nombre, esperado, obtenido):
    ok = esperado == obtenido
    resultados.append(ok)
    print(f"[{'OK' if ok else 'FALLO'}] {nombre}")
    print(f"        esperado: {esperado}")
    print(f"        obtenido: {obtenido}")


def verificar_float(nombre, esperado, obtenido, tol=1e-9):
    error = abs(esperado - obtenido)
    ok = error < tol
    resultados.append(ok)
    print(f"[{'OK' if ok else 'FALLO'}] {nombre}")
    print(f"        esperado: {esperado}   obtenido: {obtenido}   error absoluto: {error:.2e}")


def intenta_inversa(A):
    try:
        inversa_modular(A)
        return "se calculo la inversa"
    except ValueError:
        return "ValueError"


print("=== CASO 1: mensaje normal ===")
msg = "HOLA COMO ESTAS"
c = cifrar(msg)
verificar("1a. descifrar(cifrar(msg)) devuelve el mensaje original", msg, descifrar(c))
verificar("1b. primer bloque HOL -> 27 9 22 (calculado a mano)", [27, 9, 22],
          [int(x) for x in c.split()[:3]])
K = Matrix(CLAVE)
nums = a_numeros(msg)
esperado = []
for i in range(0, len(nums), N):
    esperado += [int(x) % M for x in K * Matrix(nums[i:i + N])]
verificar("1c. cifrado propio = cifrado calculado con sympy",
          " ".join(str(x) for x in esperado), c)

print("\n=== CASO 2: mensaje que no es multiplo de 3 (relleno con espacios) ===")
verificar("2. 'HOLA' se cifra con relleno y se recupera", "HOLA", descifrar(cifrar("HOLA")))

print("\n=== CASO 3 (LIMITE / ERROR): matriz sin inversa modulo 29 ===")
verificar("3a. filas proporcionales (det = 0)", "ValueError",
          intenta_inversa([[1, 2, 3], [2, 4, 6], [1, 1, 1]]))
verificar("3b. det = 29 (multiplo de 29)", "ValueError",
          intenta_inversa([[1, 0, 0], [0, 1, 0], [0, 0, 29]]))

print("\n=== CASO 4: inversa modular de la matriz clave ===")
propia = inversa_modular(CLAVE)
con_sympy = [[int(x) for x in fila] for fila in Matrix(CLAVE).inv_mod(M).tolist()]
verificar("4a. inversa propia (cofactores) = inversa de sympy", con_sympy, propia)
identidad = [[x % M for x in fila] for fila in producto(CLAVE, propia)]
verificar("4b. K x K^-1 (mod 29) = identidad", [[1, 0, 0], [0, 1, 0], [0, 0, 1]], identidad)

print("\n=== CASO 5: entradas invalidas al descifrar ===")
verificar("5a. texto no numerico", True, descifrar("hola").startswith("[Texto invalido"))
verificar("5b. cantidad de numeros no multiplo de 3", True,
          descifrar("5 10").startswith("[Mensaje incompleto"))
verificar("5c. numero fuera de rango", True,
          descifrar("5 10 99").startswith("[Numeros invalidos"))

print("\n=== CASO 6: vectores (comparacion de rostros) ===")
verificar_float("6a. distancia entre (1,2) y (4,6) = 5", 5.0,
                distancia_euclidiana([1, 2], [4, 6]))
verificar_float("6b. coseno de vectores perpendiculares = 0", 0.0,
                similitud_coseno([1, 0], [0, 1]))
verificar_float("6c. coseno de un vector consigo mismo = 1", 1.0,
                similitud_coseno([3, 4, 5], [3, 4, 5]))
rng = np.random.default_rng(0)
a, b = rng.normal(size=128), rng.normal(size=128)
verificar_float("6d. distancia propia en R^128 = numpy.linalg.norm",
                float(np.linalg.norm(a - b)), distancia_euclidiana(a, b))

print(f"\nRESULTADO: {sum(resultados)} de {len(resultados)} pruebas correctas")
