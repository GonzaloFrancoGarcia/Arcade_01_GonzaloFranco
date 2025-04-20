#!/usr/bin/env python3
import sys
import threading
import json
import traceback
from datetime import datetime

import pygame
from clients.common.network import Client

print("🚀 [DEBUG] Iniciando UI de N‑Reinas...")

def send_result(N, resuelto, pasos):
    payload = {
        'juego': 'nreinas',
        'N': N,
        'resuelto': resuelto,
        'pasos': pasos,
        'timestamp': datetime.utcnow().isoformat()
    }
    print(f"🚀 [DEBUG] Hilo enviando resultado: {payload}")
    Client().send(json.dumps(payload))

def check_solution(queens, N):
    if len(queens) != N:
        return False
    for (r1, c1) in queens:
        for (r2, c2) in queens:
            if (r1, c1) != (r2, c2):
                if r1 == r2 or c1 == c2 or abs(r1 - r2) == abs(c1 - c2):
                    return False
    return True

def main():
    print("🔧 [DEBUG] Entrando a main()")
    # Leer N desde argumento: python -m clients.nreinas.ui 8
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    print(f"▶️ [DEBUG] Tamaño N = {N}")

    SIZE = 600
    MARGIN = 50
    BOARD = SIZE - 2 * MARGIN
    CELL = BOARD // N

    pygame.init()
    print("🎨 [DEBUG] Pygame inicializado")
    screen = pygame.display.set_mode((SIZE, SIZE + 50))
    pygame.display.set_caption(f"N‑Reinas (N={N})")

    font = pygame.font.SysFont(None, 24)
    print("🔤 [DEBUG] Fuente cargada")

    queens = set()
    pasos = 0
    solved = False

    clock = pygame.time.Clock()

    while True:
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                print("🛑 [DEBUG] Cierre de ventana recibido")
                return
            if evt.type == pygame.MOUSEBUTTONDOWN and not solved:
                x, y = evt.pos
                if MARGIN <= x < MARGIN + CELL * N and MARGIN <= y < MARGIN + CELL * N:
                    c = (x - MARGIN) // CELL
                    r = (y - MARGIN) // CELL
                    if (r, c) in queens:
                        queens.remove((r, c))
                    else:
                        queens.add((r, c))
                    pasos += 1

                    if check_solution(queens, N):
                        solved = True
                        print(f"✅ [DEBUG] Solución detectada en {pasos} pasos")
                        threading.Thread(
                            target=send_result,
                            args=(N, True, pasos),
                            daemon=True
                        ).start()

        # Dibujar fondo
        screen.fill((255, 255, 255))
        # Dibujar tablero
        for r in range(N):
            for c in range(N):
                rect = pygame.Rect(
                    MARGIN + c * CELL, MARGIN + r * CELL,
                    CELL, CELL
                )
                color = (200, 200, 200) if (r + c) % 2 == 0 else (100, 100, 100)
                pygame.draw.rect(screen, color, rect)

        # Dibujar reinas
        for (r, c) in queens:
            center = (
                MARGIN + c * CELL + CELL // 2,
                MARGIN + r * CELL + CELL // 2
            )
            radius = CELL // 3
            pygame.draw.circle(screen, (255, 0, 0), center, radius)

        # Texto de pasos
        text_surf = font.render(f"Pasos: {pasos}", True, (0, 0, 0))
        screen.blit(text_surf, (10, SIZE))

        # Mensaje de resuelto
        if solved:
            msg = font.render("¡Resuelto! Resultado enviado.", True, (0, 128, 0))
            screen.blit(msg, (MARGIN, SIZE + 10))

        pygame.display.flip()
        clock.tick(30)  # limita a 30 FPS

if __name__ == '__main__':
    try:
        main()
    except Exception:
        print("❌ [ERROR] Excepción no controlada:")
        traceback.print_exc()
    finally:
        pygame.quit()
        print("🏁 [DEBUG] Pygame finalizado")
