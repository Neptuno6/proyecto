"""
Módulo de validación de reglas del juego.

Contiene las funciones para validar movimientos y prevenir islas inválidas.

Clases:
    Validation: Maneja las validaciones del tablero.

Autor: [Tu nombre]
Fecha: [Fecha]
"""

from collections import deque

class Validation:
    """
    Clase para validar las reglas del juego.
    
    Métodos:
        validate_no_islands: Verifica que no se creen islas inválidas.
    """
    
    def __init__(self):
        """Inicializa el validador."""
        pass
    
    def validate_no_islands(self, board, virus_positions, size):
        """
        Valida que al colocar una barrera no se creen islas de celdas vacías.
        
        Args:
            board (list): Matriz del tablero
            virus_positions (list): Posiciones actuales del virus
            size (int): Tamaño del tablero
            
        Returns:
            bool: True si no hay islas inválidas, False si se crean
        """
        temp_board = [row[:] for row in board]
        visited = [[False for _ in range(size)] for _ in range(size)]
        queue = deque()
        
        for x, y in virus_positions:
            queue.append((x, y))
            visited[x][y] = True
        
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        while queue:
            x, y = queue.popleft()
            
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < size and 0 <= ny < size:
                    if not visited[nx][ny] and temp_board[nx][ny] == 0:
                        visited[nx][ny] = True
                        queue.append((nx, ny))
        
        for i in range(size):
            for j in range(size):
                if temp_board[i][j] == 0 and not visited[i][j]:
                    return False
        
        return True