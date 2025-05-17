import random

class GameLogic:
    def __init__(self, size=5):
        self.size = size
        self.level = 1
        self.max_level = 3
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.barrier_placed = False
        self.barriers_remaining = self.max_barriers()
        self.initialize_level()
    
    def max_barriers(self):
        """Calcula barreras basado en tamaño del tablero y nivel"""
        base_barriers = self.size * 2  # Barreras base según tamaño
        level_multiplier = max(0.4, 1 - (self.level - 1) * 0.3)  # 30% menos por nivel
        calculated = int(base_barriers * level_multiplier)
        return max(calculated, 3)  # Mínimo 3 barreras
    
    def initialize_level(self):
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.barrier_placed = False
        self.barriers_remaining = self.max_barriers()
        initial_infections = self.level
        positions = random.sample(
            [(i, j) for i in range(self.size) for j in range(self.size)],
            initial_infections
        )
        for i, j in positions:
            self.board[i][j] = 1

    def place_barrier(self, i, j):
        if self.barriers_remaining <= 0:
            return False
            
        if self.board[i][j] == 0:
            original = self.board[i][j]
            self.board[i][j] = 2
            if not self.validate_no_islands():
                self.board[i][j] = original
                return False
            self.barrier_placed = True
            self.barriers_remaining -= 1
            return True
        return False

    def validate_no_islands(self):
        directions = [(-1,0), (1,0), (0,-1), (0,1)]
        virus_adjacent = set()
        
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 1:
                    for dx, dy in directions:
                        nx, ny = i + dx, j + dy
                        if 0 <= nx < self.size and 0 <= ny < self.size:
                            virus_adjacent.add((nx, ny))
        
        visited = [[False]*self.size for _ in range(self.size)]
        queue = []
        
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0 and (i,j) not in virus_adjacent and not visited[i][j]:
                    queue.append((i, j))
                    visited[i][j] = True
                    while queue:
                        x, y = queue.pop(0)
                        for dx, dy in directions:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < self.size and 0 <= ny < self.size:
                                if not visited[nx][ny] and self.board[nx][ny] == 0 and (nx, ny) not in virus_adjacent:
                                    visited[nx][ny] = True
                                    queue.append((nx, ny))
        
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0 and not visited[i][j] and (i,j) not in virus_adjacent:
                    return False
        return True

    def spread_virus(self):
        infected = [(i,j) for i in range(self.size) for j in range(self.size) if self.board[i][j] == 1]
        random.shuffle(infected)
        
        for x, y in infected:
            directions = random.sample([(-1,0), (1,0), (0,-1), (0,1)], 4)
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.size and 0 <= ny < self.size and self.board[nx][ny] == 0:
                    self.board[nx][ny] = 1
                    return True
        return False

    def check_win(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 1:
                    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                        ni, nj = i + dx, j + dy
                        if 0 <= ni < self.size and 0 <= nj < self.size:
                            if self.board[ni][nj] == 0:
                                return False
        return True

    def check_loss(self):
        return self.barriers_remaining <= 0 and not self.check_win()

    def advance_level(self):
        if self.level < self.max_level:
            self.level += 1
            self.initialize_level()
            return True
        return False

    def free_cells(self):
        return sum(row.count(0) for row in self.board)
