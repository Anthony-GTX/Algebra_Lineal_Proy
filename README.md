# FaceLock Hill — Biometría Facial y Mensajería Cifrada con Álgebra Lineal

> **Dos capas de seguridad, una sola base matemática:** primero tu rostro valida tu identidad en **R¹²⁸**; luego tus mensajes viajan cifrados mediante transformaciones lineales sobre **Z₂₉**.

Proyecto integrador de **Álgebra Lineal** desarrollado en **Python**, donde las operaciones matriciales y vectoriales están programadas desde cero en `matematica.py` en lugar de delegarse a funciones automáticas[cite: 1, 6].

---

## Equipo de Desarrollo

| Integrante | Carrera y Curso |
| :--- | :--- |
| **Sandra Alulema** | Ingeniería en Software — 1er Semestre "B" |
| **Joselyn Guaman** | Ingeniería en Software — 1er Semestre "B" |
| **Valentina Ortiz** | Ingeniería en Software — 1er Semestre "B" |
| **Anthony Armas** | Ingeniería en Software — 1er Semestre "B" |

---

## Cómo Funciona la Matemática por Detrás

### 1. Autenticación Facial en R¹²⁸
Cada rostro se transforma en un vector numérico de **128 dimensiones**[cite: 3, 5]:

```text
v = (v_1, v_2, ..., v_128) en R^128
```

Para comparar un rostro en vivo (`v`) contra un rostro registrado (`c`), el sistema calcula[cite: 5, 6]:

* **Distancia Euclidiana** (umbral de aceptación: `d < 0.5`)[cite: 5, 6]:
  ```text
  d(c, v) = raiz( suma_{i=1}^{128} (c_i - v_i)^2 )
  ```

* **Similitud Coseno** (mide qué tan alineados apuntan ambos vectores)[cite: 6]:
  ```text
  cos(theta) = (c · v) / (||c|| * ||v||)
  ```

### 2. Cifrado de Hill sobre Z₂₉
El alfabeto consta de **M = 29** caracteres (`A-Z`, espacio, `.` y `,`)[cite: 6]. Como `29` es primo, **Z₂₉** forma un **campo finito**, lo que permite calcular inversos modulares exactos[cite: 6].

* **Matriz clave (3 × 3):**[cite: 6]
  ```text
      | 3  3  2 |
  K = | 1  5  7 |
      | 2  8  9 |
  ```
 [cite: 6]

* **Cifrado por bloques de 3 letras** (rellenando con espacios si hace falta)[cite: 6]:
  ```text
  c_bloque = (K * p_bloque) mod 29
  ```

* **Descifrado con inversa modular** (verificando que `det(K)` sea coprimo con `29`)[cite: 5, 6]:
  ```text
  K^(-1) = (det(K)^(-1) * adj(K)) mod 29
  p_bloque = (K^(-1) * c_bloque) mod 29
  ```

---

## Estructura del Repositorio

En la raíz del repositorio se observan carpetas como `Scripts`, `__pycache__`, `reconocimiento_facial` y `re`[cite: 7], junto con los módulos principales del sistema:

```text
├── app.py              # Inicio de sesión facial y menú interactivo de mensajería
├── matematica.py       # Determinante, adjunta, inversa modular mod 29, distancia y coseno
├── registrar.py        # Captura por cámara, 68 puntos faciales y guardado en .npy
├── registrar (2).py    # Variante ligera de captura y guardado facial
├── pruebas.py          # Pruebas automáticas contrastadas con SymPy y NumPy (sin cámara)
└── requirements.txt    # Paquetes y orden de instalación recomendado
```
[cite: 1, 2, 3, 4, 5, 6]

---

## Puesta en Marcha

### 1. Preparar el entorno
```bash
git clone [https://github.com/Anthony-GTX/Algebra_Lineal_Proy.git](https://github.com/Anthony-GTX/Algebra_Lineal_Proy.git)
cd Algebra_Lineal_Proy

python -m venv venv
# Windows:
venv\Scripts\activate
# Linux / macOS:
source venv/bin/activate
```
[cite: 7]

### 2. Instalar dependencias
Sigue el orden indicado en `requirements.txt` (instalar `face_recognition` con `--no-deps` evita compilar `dlib` desde cero al usar `dlib-bin`)[cite: 4]:

```bash
pip install -r requirements.txt
pip install face_recognition_models
pip install face_recognition --no-deps
```
[cite: 4]

---

## Guía Rápida de Uso

1. **Registrar un rostro:**
   ```bash
   python registrar.py
   ```
   Escribe tu nombre sin espacios, mira a la cámara y presiona **ESPACIO** para guardar `<nombre>.npy` (o **ESC** para salir)[cite: 2, 3].

2. **Iniciar sesión y cifrar mensajes:**
   ```bash
   python app.py
   ```
   Requiere **5 coincidencias seguidas** con distancia menor a `0.5` dentro de una ventana de `15` segundos[cite: 5]. Una vez dentro, puedes enviar mensajes cifrados a `mensajes.txt`, leer/descifrar mensajes, descifrar números pegados manualmente e inspeccionar `K` y `K^(-1)` paso a paso[cite: 5].

3. **Correr las pruebas sin cámara:**
   ```bash
   python pruebas.py
   ```
   Valida cifrado/descifrado, casos de error modular, inversa contra `SymPy` y métricas vectoriales contra `NumPy`[cite: 1].

---

## Stack Tecnológico

* **Python 3** — Lenguaje principal del sistema[cite: 1, 2, 3, 5, 6].
* **NumPy** — Vectores en **R¹²⁸** y comprobación numérica[cite: 1, 2, 3, 5, 6].
* **OpenCV (`opencv-python`)** — Video en tiempo real y anotaciones en pantalla[cite: 2, 3, 4, 5]
