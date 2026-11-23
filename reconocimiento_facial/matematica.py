"""
matematica.py - Funciones de Algebra Lineal del proyecto.
No usa camara ni librerias de rostros, por eso se puede probar sola (ver pruebas.py).
"""
from math import gcd
import numpy as np

# ---------- ALFABETO Y MATRIZ CLAVE (CIFRADO DE HILL) ----------
ALFABETO = "ABCDEFGHIJKLMNOPQRSTUVWXYZ .,"
M = len(ALFABETO)            # 29 (numero primo: Z_29 es un campo)
CLAVE = [[3, 3, 2],
         [1, 5, 7],
         [2, 8, 9]]
N = len(CLAVE)               # tamano de bloque (3)


# ---------- OPERACIONES CON MATRICES (HECHAS A MANO) ----------
def menor(A, i, j):
    """Matriz A sin la fila i ni la columna j."""
    return [fila[:j] + fila[j + 1:] for k, fila in enumerate(A) if k != i]


def determinante(A):
    """Determinante por expansion de cofactores sobre la primera fila."""
    n = len(A)
    if n == 1:
        return A[0][0]
    if n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    return sum((-1) ** j * A[0][j] * determinante(menor(A, 0, j)) for j in range(n))


def adjunta(A):
    """Matriz adjunta = transpuesta de la matriz de cofactores."""
    n = len(A)
    cof = [[(-1) ** (i + j) * determinante(menor(A, i, j)) for j in range(n)]
           for i in range(n)]
    return [[cof[j][i] for j in range(n)] for i in range(n)]


def producto(A, B):
    """Producto de matrices A x B."""
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))]
            for i in range(len(A))]


def inversa_modular(A, m=M):
    """Inversa de A modulo m: K^-1 = det(K)^-1 * adj(K) (mod m).
    Lanza ValueError si det(K) no es invertible modulo m."""
    det = determinante(A) % m
    if det == 0 or gcd(det, m) != 1:
        raise ValueError(f"La matriz no tiene inversa modulo {m} (det mod {m} = {det})")
    det_inv = pow(det, -1, m)            # inverso de det modulo m
    return [[(det_inv * x) % m for x in fila] for fila in adjunta(A)]


def mat_por_vector(A, v, m=M):
    """A * v (mod m)."""
    return [sum(A[i][j] * v[j] for j in range(len(v))) % m for i in range(len(A))]


CLAVE_INV = inversa_modular(CLAVE)


# ---------- CIFRADO Y DESCIFRADO ----------
def a_numeros(texto):
    """Convierte el texto en numeros segun el alfabeto (ignora otros caracteres)."""
    return [ALFABETO.index(c) for c in texto.upper() if c in ALFABETO]


def procesar(nums, matriz):
    """Multiplica cada bloque de N numeros por la matriz (mod 29)."""
    resultado = []
    for i in range(0, len(nums), N):
        resultado += mat_por_vector(matriz, nums[i:i + N])
    return resultado


def cifrar(texto):
    """C = K * P (mod 29). Devuelve los numeros separados por espacios."""
    nums = a_numeros(texto)
    while len(nums) % N:                 # relleno con espacios
        nums.append(ALFABETO.index(" "))
    return " ".join(str(x) for x in procesar(nums, CLAVE))


def descifrar(texto):
    """P = K^-1 * C (mod 29). Valida la entrada antes de calcular."""
    try:
        nums = [int(x) for x in texto.replace(",", " ").split()]
    except ValueError:
        return "[Texto invalido: solo deben ser numeros]"
    if len(nums) == 0 or len(nums) % N != 0:
        return f"[Mensaje incompleto: la cantidad de numeros debe ser multiplo de {N}]"
    if any(x < 0 or x >= M for x in nums):
        return f"[Numeros invalidos: deben estar entre 0 y {M - 1}]"
    return "".join(ALFABETO[x] for x in procesar(nums, CLAVE_INV)).strip()


# ---------- VECTORES (COMPARACION DE ROSTROS) ----------
def producto_escalar(a, b):
    return float(np.sum(np.asarray(a, dtype=float) * np.asarray(b, dtype=float)))


def magnitud(v):
    return float(np.sqrt(producto_escalar(v, v)))


def distancia_euclidiana(a, b):
    """d = raiz( suma de (a_i - b_i)^2 )."""
    dif = np.asarray(a, dtype=float) - np.asarray(b, dtype=float)
    return float(np.sqrt(np.sum(dif ** 2)))


def similitud_coseno(a, b):
    """cos(theta) = (a . b) / (|a| |b|)."""
    return producto_escalar(a, b) / (magnitud(a) * magnitud(b))
