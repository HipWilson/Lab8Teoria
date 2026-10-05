"""Ejecuta los programas en C, mide tiempos y genera tablas (CSV) y graficas (PNG).
Uso:  python3 profiling.py
Requiere: gcc, python3, matplotlib
"""
import subprocess, statistics, csv, os, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

NS = [1, 10, 100, 1000, 10000, 100000, 1000000]
AQUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(AQUI, "..", "resultados")
os.makedirs(OUT, exist_ok=True)

# Operaciones teoricas T(n) ~ c * f(n) para extrapolar lo que no es practico ejecutar
MODELOS = {
    1: ("O(n^2 log n)", lambda n: n * n * (math.log2(n) if n > 1 else 1)),
    2: ("O(n)",         lambda n: n),
    3: ("O(n^2)",       lambda n: n * n),
}
# Si estimar el tiempo supera este limite (segundos) NO se ejecuta, se extrapola
LIMITE_S = 400
CONST_NS = {1: 1.7e-9, 2: 3e-9, 3: 1.7e-9}  # costo por operacion elemental (aprox. para decidir)

def correr(p, n):
    exe = os.path.join(AQUI, f"problema{p}")
    r = subprocess.run([exe, str(n)], capture_output=True, text=True, check=True)
    n_, cnt, t = r.stdout.strip().split(",")
    return int(cnt), float(t)

for p in (1, 2, 3):
    subprocess.run(["gcc", "-O0", "-o", os.path.join(AQUI, f"problema{p}"),
                    os.path.join(AQUI, f"problema{p}.c")], check=True)

for p, (nombre, f) in MODELOS.items():
    filas, medidos = [], []
    for n in NS:
        est = CONST_NS[p] * f(n)
        if est > LIMITE_S:
            filas.append((n, None, None, "extrapolado"))
            continue
        reps = 5 if est < 1 else 1
        res = [correr(p, n) for _ in range(reps)]
        cnt = res[0][0]
        t = statistics.median(r[1] for r in res)
        filas.append((n, cnt, t, "medido"))
        medidos.append((n, t))
        print(f"P{p} n={n} cnt={cnt} t={t:.6f}s", flush=True)
    # constante c = t / f(n) usando la mayor n medida con t suficientemente grande
    base = [(n, t) for n, t in medidos if t > 1e-3] or medidos[-1:]
    c = statistics.median(t / f(n) for n, t in base)
    filas2 = []
    for n, cnt, t, est in filas:
        if t is None:
            t = c * f(n)
        filas2.append((n, cnt, t, est))
    with open(os.path.join(OUT, f"problema{p}.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["n", "operaciones", "tiempo_s", "origen"])
        for n, cnt, t, o in filas2:
            w.writerow([n, cnt if cnt is not None else "", f"{t:.9f}", o])
    # grafica lineal y log-log
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    ns = [r[0] for r in filas2]; ts = [r[2] for r in filas2]
    med = [r for r in filas2 if r[3] == "medido"]; ext = [r for r in filas2 if r[3] != "medido"]
    for a, log in zip(ax, (False, True)):
        a.plot(ns, ts, "-", color="gray", alpha=.5)
        a.plot([r[0] for r in med], [r[2] for r in med], "o", color="tab:blue", label="medido")
        if ext:
            a.plot([r[0] for r in ext], [r[2] for r in ext], "s", color="tab:red", label="extrapolado")
        a.set_xlabel("tamano de entrada n"); a.set_ylabel("tiempo (s)"); a.grid(True, alpha=.3)
        if log:
            a.set_xscale("log"); a.set_yscale("log"); a.set_title(f"Problema {p} (log-log) - {nombre}")
        else:
            a.set_title(f"Problema {p} - {nombre}")
        a.legend()
    plt.tight_layout(); plt.savefig(os.path.join(OUT, f"problema{p}.png"), dpi=130); plt.close()
print("Listo. Resultados en", os.path.abspath(OUT))
