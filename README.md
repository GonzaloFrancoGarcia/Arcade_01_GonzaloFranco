# Máquina Arcade Distribuida

Este proyecto implementa una “Máquina Arcade” distribuida en Python, compuesta por tres juegos clásicos de raíces algorítmicas:

- **N‑Reinas**  
- **Knight’s Tour**  
- **Torres de Hanói**  

Cada juego corre como un cliente independiente con interfaz en Pygame, y un servidor central recibe y almacena los resultados en una base de datos SQLite mediante SQLAlchemy.

---

## 📁 Estructura de carpetas

```plaintext
Arcade_01_GonzaloFranco/
├── README.md
├── requirements.txt
├── launcher.py
├── server/
│   ├── __init__.py
│   ├── main.py
│   ├── network.py
│   ├── models.py
│   └── db.py
├── clients/
│   ├── common/
│   │   ├── __init__.py
│   │   └── network.py
│   ├── nreinas/
│   │   ├── __init__.py
│   │   ├── game.py
│   │   └── ui.py
│   ├── caballo/
│   │   ├── __init__.py
│   │   ├── game.py
│   │   └── ui.py
│   └── hanoi/
│       ├── __init__.py
│       ├── game.py
│       └── ui.py
└── docs/
    └── informe.pdf
