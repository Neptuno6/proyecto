"""
Módulo de lógica del juego Virus Spread Challenge.

Contiene la implementación de las reglas del juego, estado del tablero,
mecánicas de propagación del virus y manejo de niveles.

Clases:
    GameLogic: Maneja toda la lógica del juego y estado actual.

Autor: [Tu nombre]
Fecha: [Fecha]
"""

import random
from validation import Validation

class GameLogic:
    """
    Clase que maneja la lógica principal del juego.
    
    Atributos:
        size (int): Tamaño del tablero (NxN)
        level (int): Nivel actual del juego
        board (list): Matriz que representa el estado del tablero
        virus_positions (list): Lista de tuplas con posiciones de virus
        turn (int): Número de turno actual
        game_over (bool): Indica si el juego ha terminado
        winner (str): Indica el ganador ('player' o 'virus')
        validator (Validation): Instancia para validar movimientos
    """
    
    def __init__(self, size=10):
        """
        Inicializa la lógica del juego con un tablero vacío.
        
        Args:
            size (int): Tamaño del tablero (por defecto 10x10)
        """
        self.size = size
        self.level = 1
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.virus_positions = []
        self.turn = 0
        self.game_over = False
        self.winner = None
        self.validator = Validation()
        self.initialize_infection_points()
    
    def initialize_infection_points(self):
        """Coloca los puntos de infección iniciales según el nivel actual."""
        self.virus_positions = []
        for _ in range(self.level):
            while True:
                x, y = random.randint(0, self.size-1), random.randint(0, self.size-1)
                if self.board[x][y] == 0:  # Celda libre
                    self.board[x][y] = 1
                    self.virus_positions.append((x, y))
                    break
    
    def place_barrier(self, x, y):
        """
        Intenta colocar una barrera en la posición (x, y).
        
        Args:
            x (int): Coordenada x de la celda
            y (int): Coordenada y de la celda
            
        Returns:
            bool: True si la barrera se colocó exitosamente, False si no
        """
        if self.game_over or self.board[x][y] != 0:
            return False
        
        temp_board = [row[:] for row in self.board]
        temp_board[x][y] = 2  # Barrera
        
        if self.validator.validate_no_islands(temp_board, self.virus_positions, self.size):
            self.board[x][y] = 2
            return True
        return False
    
    def spread_virus(self):
        """Propaga el virus a celdas adyacentes según las reglas del juego."""
        if self.game_over:
            return
        
        new_infections = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # derecha, abajo, izquierda, arriba
        
        for x, y in self.virus_positions:
            random.shuffle(directions)
            
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.size and 0 <= ny < self.size and self.board[nx][ny] == 0:
                    self.board[nx][ny] = 1
                    new_infections.append((nx, ny))
                    break  # Solo una infección por virus por turno
        
        self.virus_positions.extend(new_infections)
        self.turn += 1
        self.check_game_status()
    
    def check_game_status(self):
        """Verifica si el juego ha terminado y determina el ganador."""
        can_spread = False
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        for x, y in self.virus_positions:
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.size and 0 <= ny < self.size and self.board[nx][ny] == 0:
                    can_spread = True
                    break
            if can_spread:
                break
        
        if not can_spread:
            self.game_over = True
            self.winner = "player"
            return
        
        free_cells = sum(row.count(0) for row in self.board)
        if free_cells == 0:
            self.game_over = True
            self.winner = "virus"
    
    def next_level(self):
        """
        Avanza al siguiente nivel del juego si el jugador ganó.
        
        Returns:
            bool: True si se avanzó de nivel, False si no
        """
        if self.game_over and self.winner == "player":
            self.level += 1
            self.reset_board()
            return True
        return False
    
    def reset_board(self):
        """Reinicia el tablero para un nuevo nivel."""
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.virus_positions = []
        self.turn = 0
        self.game_over = False
        self.winner = None
        self.initialize_infection_points()
    
    def get_board_state(self):
        """
        Obtiene el estado actual del tablero.
        
        Returns:
            list: Copia de la matriz del tablero
        """
        return [row[:] for row in self.board]