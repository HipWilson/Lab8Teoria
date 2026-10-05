# Laboratorio 8 — Teoría de la computación

Análisis de complejidad, profiling y respuestas teóricas.

## Estructura
```
codigo/             Programas en C (problema1-3), profiling.py
resultados/         Tablas (CSV) y gráficas (PNG) de los Problemas 1, 2 y 3
respuestas_pdf/     Respuestas sin código (Problemas 1-5) en PDF
```

## Instrucciones de ejecución
Requisitos: `gcc`, `python3`, `matplotlib` (`pip install matplotlib`).

```bash
cd codigo
python3 profiling.py
```
El script compila los tres programas (`gcc -O0`), los ejecuta con n = 1, 10, 100, 1000, 10000, 100000, 1000000,
y genera `resultados/problemaX.csv` y `resultados/problemaX.png`.

También se puede ejecutar un programa individual:
```bash
gcc -O0 -o problema3 problema3.c
./problema3 10000        # imprime: n,operaciones,tiempo_en_segundos
```

## Notas
- En los Problemas 2 y 3 el `printf("Sequence\n")` se sustituye por un contador, para medir el algoritmo y no la consola.
- Tiempos para n = 1,000,000 en los Problemas 1 y 3 son **extrapolados** (marcados en rojo en las gráficas) porque
  requieren ~5×10^12 y ~8×10^10 operaciones; el resto son medidos.
- Tiempo medido en una máquina concreta; los valores absolutos varían, la tendencia (n² log n, n, n²) no.

## Video de demostración
YouTube (no listado): **PEGAR_AQUI_EL_ENLACE**

## Respuestas
Ver `respuestas_pdf/Respuestas_Laboratorio8.pdf`.
