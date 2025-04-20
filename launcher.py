#!/usr/bin/env python3
import sys
import subprocess

def main():
    while True:
        print("\n=== Máquina Arcade Distribuida ===")
        print("1) N‑Reinas")
        print("2) Knight’s Tour")
        print("3) Torres de Hanói")
        print("4) Salir")
        choice = input("Selecciona un juego [1‑4]: ").strip()

        if choice == "1":
            n = input("  Introduce N (por defecto 8): ").strip() or "8"
            subprocess.Popen([sys.executable, "-m", "clients.nreinas.ui", n])

        elif choice == "2":
            print("  (Elige casilla inicial dentro de la ventana)")
            subprocess.Popen([sys.executable, "-m", "clients.caballo.ui"])

        elif choice == "3":
            d = input("  ¿Cuántos discos? (por defecto 3): ").strip() or "3"
            subprocess.Popen([sys.executable, "-m", "clients.hanoi.ui", d])

        elif choice == "4":
            print("Saliendo. ¡Hasta luego!")
            sys.exit(0)

        else:
            print("Opción no válida, elige 1‑4.")

if __name__ == "__main__":
    main()
