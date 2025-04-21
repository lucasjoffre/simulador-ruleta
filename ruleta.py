import random
import argparse
import matplotlib.pyplot as plt
import numpy as np
import os

def simular_ruleta(n_tiradas, numero_elegido):
    resultados = []
    frn = []
    vp = []
    vd = []
    vv = []

    contador_elegido = 0

    for i in range(1, n_tiradas + 1):
        tirada = random.randint(0, 36)
        resultados.append(tirada)

        # Frecuencia relativa del número elegido
        if tirada == numero_elegido:
            contador_elegido += 1
        frn.append(contador_elegido / i)

        # Valor promedio
        vp.append(np.mean(resultados))

        # Desvío estándar
        vd.append(np.std(resultados))

        # Varianza
        vv.append(np.var(resultados))

    return frn, vp, vd, vv

def graficar_una_corrida(n_tiradas, numero_elegido, corrida_id, frn, vp, vd, vv):
    x = list(range(1, n_tiradas + 1))
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle(f'Corrida {corrida_id + 1} - Análisis estadístico del número {numero_elegido}', fontsize=14)

    # Frecuencia relativa
    axs[0, 0].plot(x, frn, label="frn", color="red")
    axs[0, 0].axhline(1/37, color='blue', linestyle='--', label="fre esperada")
    axs[0, 0].set_title("Frecuencia Relativa")
    axs[0, 0].set_xlabel("n (tiradas)")
    axs[0, 0].set_ylabel("frecuencia relativa")
    axs[0, 0].legend()
    axs[0, 0].grid(True)

    # Promedio
    axs[0, 1].plot(x, vp, label="vpn", color="red")
    axs[0, 1].axhline(18, color='blue', linestyle='--', label="vpe (esperado)")
    axs[0, 1].set_title("Valor Promedio")
    axs[0, 1].set_xlabel("n (tiradas)")
    axs[0, 1].set_ylabel("valor promedio")
    axs[0, 1].legend()
    axs[0, 1].grid(True)

    # Desvío estándar
    axs[1, 0].plot(x, vd, label="vd", color="red")
    axs[1, 0].axhline(np.std(range(37)), color='blue', linestyle='--', label="vde (esperado)")
    axs[1, 0].set_title("Desvío Estándar")
    axs[1, 0].set_xlabel("n (tiradas)")
    axs[1, 0].set_ylabel("desvío")
    axs[1, 0].legend()
    axs[1, 0].grid(True)

    # Varianza
    axs[1, 1].plot(x, vv, label="vvn", color="red")
    axs[1, 1].axhline(np.var(range(37)), color='blue', linestyle='--', label="vve (esperada)")
    axs[1, 1].set_title("Varianza")
    axs[1, 1].set_xlabel("n (tiradas)")
    axs[1, 1].set_ylabel("varianza")
    axs[1, 1].legend()
    axs[1, 1].grid(True)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(f'grafica_corrida_{corrida_id+1}.png')
    plt.show()

def graficar_comparativa_corridas(lista_de_resultados, titulo, esperado=None, ylabel=""):
    plt.figure(figsize=(10, 6))
    for i, datos in enumerate(lista_de_resultados):
        plt.plot(range(1, len(datos) + 1), datos, label=f'Corrida {i+1}')
    if esperado is not None:
        plt.axhline(esperado, color='blue', linestyle='--', label='Esperado')
    plt.title(titulo)
    plt.xlabel('n (tiradas)')
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)
    plt.savefig(f'comparativa_{titulo.replace(" ", "_").lower()}.png')
    plt.show()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', type=int, default=1, help='Cantidad de corridas')
    parser.add_argument('-n', type=int, required=True, help='Cantidad de tiradas por corrida')
    parser.add_argument('-e', type=int, required=True, help='Número elegido (0-36)')
    args = parser.parse_args()

    frn_todas = []
    vp_todas = []
    vd_todas = []
    vv_todas = []

    for i in range(args.c):
        frn, vp, vd, vv = simular_ruleta(args.n, args.e)
        if args.c == 1:
            graficar_una_corrida(args.n, args.e, i, frn, vp, vd, vv)
        else:
            frn_todas.append(frn)
            vp_todas.append(vp)
            vd_todas.append(vd)
            vv_todas.append(vv)

    if args.c > 1:
        graficar_comparativa_corridas(frn_todas, "Frecuencia Relativa", esperado=1/37, ylabel="Frecuencia Relativa")
        graficar_comparativa_corridas(vp_todas, "Valor Promedio", esperado=18, ylabel="Promedio")
        graficar_comparativa_corridas(vd_todas, "Desvío Estándar", esperado=np.std(range(37)), ylabel="Desvío")
        graficar_comparativa_corridas(vv_todas, "Varianza", esperado=np.var(range(37)), ylabel="Varianza")

if __name__ == "__main__":
    main()
