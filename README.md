# Laboratorio 8 — Teoría de la computación

Análisis de complejidad de algoritmos (notación Big-Oh), profiling de tres programas en C y respuestas teóricas.

## Video de demostración
[Ver video](https://youtu.be/CMQyr7csGZ4)


## Estructura del repositorio
```
codigo/             problema1.c, problema2.c, problema3.c y profiling.py (menú)
resultados/         Tablas (CSV) y gráficas (PNG) de los Problemas 1, 2 y 3
respuestas_pdf/     Respuestas sin código (Problemas 1 al 5) en PDF
```

## Requisitos
- `gcc` (compilador de C)
- `python` 3
- `matplotlib`:
  ```bash
  pip install matplotlib
  ```

## Cómo ejecutar
```bash
cd codigo
python profiling.py
```
Se abre un menú para elegir qué problema correr:

```
1) Problema 1  O(n^2 log n)   
2) Problema 2  O(n)           
3) Problema 3  O(n^2)         
4) Correr los tres
0) Salir
```
Al elegir una opción, el script:
1. Compila el archivo `.c` del problema con `gcc -O0`.
2. Lo ejecuta con n = 1, 10, 100, 1000, 10000, 100000 y 1000000.
3. Muestra la tabla en la terminal (n, operaciones, tiempo y cuántas veces crece el tiempo al multiplicar n por 10).
4. Guarda `resultados/problemaX.csv` y `resultados/problemaX.png`, y ofrece abrir la gráfica.

También se puede ejecutar un programa individual (imprime `n,operaciones,tiempo_en_segundos`):
```bash
gcc -O0 -o problema3 problema3.c
./problema3 10000        
```

## Resumen de resultados

| Problema | Complejidad | Operaciones |
|---|---|---|
| 1 | Θ(n² log n) | (n/2+1)(n/2)(⌊log₂ n⌋+1) |
| 2 | Θ(n) | n (el `break` deja el ciclo interno en una vuelta) |
| 3 | Θ(n²) | ⌊n/3⌋·⌈n/4⌉ ≈ n²/12 |

El procedimiento completo de los Problemas 1 al 5 (incluido Problema 4: búsqueda lineal, búsqueda binaria y Quick Sort) está en
`respuestas_pdf/Respuestas_Laboratorio8.pdf`.

## Notas
- En los Problemas 2 y 3 el `printf("Sequence\n")` se sustituye por un contador, para medir el algoritmo y no la consola.
- Los tiempos para n = 1,000,000 en los Problemas 1 y 3 son extrapolados, porque requieren ~5×10¹² y ~8×10¹⁰ operaciones. El resto son mediciones reales.
- Los tiempos dependen de la computadora; lo importante es la tendencia de crecimiento (n² log n, n y n²).
