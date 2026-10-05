
import subprocess, statistics, csv, os, math, sys, time
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

NS = [1, 10, 100, 1000, 10000, 100000, 1000000]
AQUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(AQUI, "..", "resultados"))
EXT = ".exe" if os.name == "nt" else ""

# nombre, f(n) para extrapolar, costo aprox. por operacion (s), descripcion
PROBLEMAS = {
    1: ("O(n^2 log n)", lambda n: n * n * (math.log2(n) if n > 1 else 1), 4.2e-10,
        "tres ciclos anidados: n/2 * n/2 * log2(n)"),
    2: ("O(n)", lambda n: n, 2.4e-9,
        "ciclo doble con break: n * 1"),
    3: ("O(n^2)", lambda n: n * n, 1.5e-10,
        "n/3 * n/4 = n^2 / 12"),
}
LIMITE_S = 100  # si el tiempo estimado supera esto, NO se ejecuta


def compilar(p):
    src = os.path.join(AQUI, f"problema{p}.c")
    exe = os.path.join(AQUI, f"problema{p}{EXT}")
    if not os.path.exists(src):
        sys.exit(f"\nERROR: no se encontro {src}. Deja profiling.py en la misma carpeta que problema1.c, problema2.c y problema3.c")
    try:
        subprocess.run(["gcc", "-O0", "-o", exe, src], check=True)
    except FileNotFoundError:
        sys.exit("\nERROR: no se encontro 'gcc'. Instalalo y vuelve a intentar")
    return exe


def correr(exe, n):
    r = subprocess.run([exe, str(n)], capture_output=True, text=True, check=True)
    _, cnt, t = r.stdout.strip().split(",")
    return int(cnt), float(t)


def fmt_t(t):
    if t < 1e-3:  return f"{t * 1e6:.2f} us"
    if t < 1:     return f"{t * 1e3:.2f} ms"
    if t < 120:   return f"{t:.2f} s"
    if t < 7200:  return f"{t / 60:.1f} min"
    return f"{t / 3600:.1f} h"


def imprimir_tabla(p, filas):
    nombre = PROBLEMAS[p][0]
    print(f"\n  RESULTADOS - Problema {p}  ->  {nombre}")
    print("  " + "-" * 78)
    print(f"  {'n':>10} | {'operaciones':>16} | {'tiempo':>12} | {'x vs anterior':>13} | origen")
    print("  " + "-" * 78)
    prev = None
    for n, cnt, t, origen in filas:
        ops = f"{cnt:,}" if cnt is not None else "-"
        ratio = f"x{t / prev:.1f}" if prev and prev >= 1e-5 else "-"
        print(f"  {n:>10,} | {ops:>16} | {fmt_t(t):>12} | {ratio:>13} | {origen}")
        prev = t
    print("  " + "-" * 78)
    esperado = {1: "un poco mas de x100", 2: "cerca de x10", 3: "cerca de x100"}[p]
    print(f"  Al multiplicar n por 10 el tiempo deberia crecer {esperado}  ({nombre}).")


def guardar(p, filas):
    os.makedirs(OUT, exist_ok=True)
    nombre = PROBLEMAS[p][0]
    with open(os.path.join(OUT, f"problema{p}.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["n", "operaciones", "tiempo_s", "origen"])
        for n, cnt, t, o in filas:
            w.writerow([n, cnt if cnt is not None else "", f"{t:.9f}", o])
    ns = [r[0] for r in filas]; ts = [r[2] for r in filas]
    med = [r for r in filas if r[3] == "medido"]
    ext = [r for r in filas if r[3] != "medido"]
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    for a, log in zip(ax, (False, True)):
        a.plot(ns, ts, "-", color="gray", alpha=.5)
        a.plot([r[0] for r in med], [r[2] for r in med], "o", color="tab:blue", label="medido")
        if ext:
            a.plot([r[0] for r in ext], [r[2] for r in ext], "s", color="tab:red", label="extrapolado")
        a.set_xlabel("tamano de entrada n"); a.set_ylabel("tiempo (s)"); a.grid(True, alpha=.3)
        if log:
            a.set_xscale("log"); a.set_yscale("log")
            a.set_title(f"Problema {p} (log-log) - {nombre}")
        else:
            a.set_title(f"Problema {p} - {nombre}")
        a.legend()
    plt.tight_layout()
    png = os.path.join(OUT, f"problema{p}.png")
    plt.savefig(png, dpi=130); plt.close()
    return png


def ejecutar(p):
    nombre, f, costo, desc = PROBLEMAS[p]
    print(f"\n{'=' * 80}\n  PROBLEMA {p}  -  {nombre}   ({desc})\n{'=' * 80}")
    exe = compilar(p)
    print("  Compilado con gcc -O0. Midiendo...\n")
    filas, medidos = [], []
    for n in NS:
        est = costo * f(n)
        if est > LIMITE_S:
            print(f"  n = {n:>9,}  -> demasiado largo (~{fmt_t(est)}), se EXTRAPOLA", flush=True)
            filas.append([n, None, None, "extrapolado"])
            continue
        if est > 10:
            print(f"  n = {n:>9,}  -> midiendo, tardara ~{fmt_t(est)}...", flush=True)
        reps = 5 if est < 1 else 1
        res = [correr(exe, n) for _ in range(reps)]
        t = statistics.median(r[1] for r in res)
        filas.append([n, res[0][0], t, "medido"])
        medidos.append((n, t))
        print(f"  n = {n:>9,}  -> {fmt_t(t):>10}", flush=True)
    base = [(n, t) for n, t in medidos if t > 1e-3] or medidos[-1:]
    c = statistics.median(t / f(n) for n, t in base)
    for r in filas:
        if r[2] is None:
            r[2] = c * f(r[0])
    imprimir_tabla(p, filas)
    png = guardar(p, filas)
    print(f"\n  Guardado: resultados/problema{p}.csv  y  {os.path.relpath(png, AQUI)}")
    return png


def abrir(png):
    try:
        if os.name == "nt":
            os.startfile(png)
        elif sys.platform == "darwin":
            subprocess.run(["open", png])
        else:
            subprocess.run(["xdg-open", png])
    except Exception:
        print("  No pude abrir la grafica automaticamente, abrela desde la carpeta resultados.")


def menu():
    print("\n" + "=" * 80)
    print("   LABORATORIO 8 - PROFILING")
    print("=" * 80)
    print("   1) Problema 1  O(n^2 log n)   ")
    print("   2) Problema 2  O(n)          ")
    print("   3) Problema 3  O(n^2)         ")
    print("   4) Correr los tres")
    print("   0) Salir")
    return input("\n   Elige una opcion: ").strip()


def main():
    while True:
        op = menu()
        if op == "0":
            print("\n  Hasta luego.\n"); return
        if op in ("1", "2", "3"):
            pngs = [ejecutar(int(op))]
        elif op == "4":
            pngs = [ejecutar(p) for p in (1, 2, 3)]
        else:
            print("\n  Opcion no valida. Escribe 0, 1, 2, 3 o 4.")
            continue
        if input("\n  Abrir la(s) grafica(s)? (s/n): ").strip().lower() == "s":
            for png in pngs:
                abrir(png)
        input("\n  Presiona Enter para volver al menu...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Interrumpido.\n")