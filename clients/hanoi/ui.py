#!/usr/bin/env python3
import sys
import threading
import json
from datetime import datetime
import traceback

import pygame
from clients.common.network import Client

def send_result(discos, movimientos, resuelto):
    payload = {
        'juego': 'hanoi',
        'discos': discos,
        'movimientos': movimientos,
        'resuelto': resuelto,
        'timestamp': datetime.utcnow().isoformat()
    }
    Client().send(json.dumps(payload))

def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3

    SIZE = 600
    MARGIN = 50
    BASE_Y = SIZE - MARGIN // 2
    PEGS_X = [
        MARGIN + (SIZE-2*MARGIN)//4*0,
        MARGIN + (SIZE-2*MARGIN)//4*1,
        MARGIN + (SIZE-2*MARGIN)//4*2
    ]

    pygame.init()
    screen = pygame.display.set_mode((SIZE, SIZE))
    pygame.display.set_caption("Torres de Hanói")
    font = pygame.font.SysFont(None, 24)

    # Inicializa varillas: A, B, C
    pegs = {0: list(range(n,0,-1)), 1: [], 2: []}
    movimientos = 0
    selected = None  # índice de pega seleccionada

    clock = pygame.time.Clock()

    def draw():
        screen.fill((255,255,255))
        # Dibujar varillas
        for i,x in enumerate(PEGS_X):
            pygame.draw.line(screen, (0,0,0), (x, MARGIN), (x, BASE_Y), 5)
            # Dibujar discos
            stack = pegs[i]
            for depth, size in enumerate(stack):
                w = size * 20
                h = 20
                rect = pygame.Rect(
                    x - w//2,
                    BASE_Y - (depth+1)*h,
                    w, h
                )
                color = (150, 150 + size*5, 200 - size*5)
                pygame.draw.rect(screen, color, rect)
        # Texto
        txt = font.render(f"Movimientos: {movimientos}", True, (0,0,0))
        screen.blit(txt, (10,10))

    running = True
    while running:
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                running = False

            if evt.type == pygame.MOUSEBUTTONDOWN:
                mx,my = evt.pos
                # Detectar peg clicada
                for i,x in enumerate(PEGS_X):
                    if abs(mx-x) < 30:
                        if selected is None and pegs[i]:
                            selected = i
                        elif selected is not None:
                            if not pegs[i] or pegs[selected][-1] < pegs[i][-1]:
                                # Mover disco
                                disk = pegs[selected].pop()
                                pegs[i].append(disk)
                                movimientos += 1
                                selected = None
                            else:
                                selected = None
                        break

                # Comprobar si está resuelto: todos en la tercera varilla
                if len(pegs[2]) == n:
                    # Enviar resultado en hilo
                    threading.Thread(
                        target=send_result,
                        args=(n, movimientos, True),
                        daemon=True
                    ).start()
                    print("✅ Resuelto y enviado")
                    running = False

        draw()
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == '__main__':
    try:
        main()
    except Exception:
        traceback.print_exc()
        pygame.quit()
