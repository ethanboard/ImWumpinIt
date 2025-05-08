import random

GRID_SIZE = 5
NUM_BATS = 2
NUM_PITS = 2

class Game:
    def __init__(self):
        self.reset()

    def reset(self):
        self.grid = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.player_pos = self.random_empty_cell()
        self.wumpus_pos = self.place('W')
        self.bats_pos = [self.place('B') for _ in range(NUM_BATS)]
        self.pits_pos = [self.place('P') for _ in range(NUM_PITS)]
        self.game_over = False
        self.arrows = 3

    def random_empty_cell(self):
        while True:
            x = random.randint(0, GRID_SIZE - 1)
            y = random.randint(0, GRID_SIZE - 1)
            if self.grid[y][x] == '':
                return (x, y)

    def place(self, marker):
        x, y = self.random_empty_cell()
        self.grid[y][x] = marker
        return (x, y)

    def is_adjacent(self, pos1, pos2):
        dx = abs(pos1[0] - pos2[0])
        dy = abs(pos1[1] - pos2[1])
        return (dx == 1 and dy == 0) or (dx == 0 and dy == 1)

    def get_cues(self):
        cues = []
        for hazard_pos, message in [
            (self.wumpus_pos, "You smell a Wumpus."),
            *[(pos, "You hear flapping.") for pos in self.bats_pos],
            *[(pos, "You feel a breeze.") for pos in self.pits_pos],
        ]:
            if self.is_adjacent(self.player_pos, hazard_pos):
                cues.append(message)
        return cues

    def move_player(self, direction):
        x, y = self.player_pos
        if direction == 'W' and y > 0:
            y -= 1
        elif direction == 'S' and y < GRID_SIZE - 1:
            y += 1
        elif direction == 'A' and x > 0:
            x -= 1
        elif direction == 'D' and x < GRID_SIZE - 1:
            x += 1
        else:
            print("You hit a wall!")
            return
        self.player_pos = (x, y)
        self.check_current_tile()

    def check_current_tile(self):
        x, y = self.player_pos
        tile = self.grid[y][x]
        if tile == 'W':
            print("You walked into the Wumpus... CHOMP! Game over.")
            self.game_over = True
        elif tile == 'P':
            print("You fell into a pit... Game over.")
            self.game_over = True
        elif tile == 'B':
            print("Bats snatch you and drop you somewhere else!")
            self.player_pos = self.random_empty_cell()
            self.check_current_tile()  # recursive re-check

    def shoot_arrow(self, direction):
        if self.arrows <= 0:
            print("You're out of arrows!")
            return

        self.arrows -= 1
        x, y = self.player_pos

        print(f"You shoot an arrow to the {direction}...")

        while 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
            if (x, y) == self.wumpus_pos:
                print("Your arrow hits the Wumpus! You win!")
                self.game_over = True
                return
            if direction == 'W':
                y -= 1
            elif direction == 'S':
                y += 1
            elif direction == 'A':
                x -= 1
            elif direction == 'D':
                x += 1

        print("Missed! The Wumpus wakes up and moves...")
        self.move_wumpus()

    def move_wumpus(self):
        # Move Wumpus to a random adjacent cell
        x, y = self.wumpus_pos
        directions = [(0,1), (1,0), (0,-1), (-1,0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and self.grid[ny][nx] == '':
                self.grid[y][x] = ''
                self.wumpus_pos = (nx, ny)
                self.grid[ny][nx] = 'W'
                return

    def display_player_view(self):
        print(f"\nYou are at position {self.player_pos}")
        print(f"Arrows remaining: {self.arrows}")
        for cue in self.get_cues():
            print(cue)

def main():
    while True:
        game = Game()
        print("\nWelcome to Hunt the Wumpus! Use W/A/S/D to move, F + direction to shoot.")
        while not game.game_over:
            game.display_player_view()
            move = input("Move (W/A/S/D) or Shoot (F+W/A/S/D): ").strip().upper()

            if move.startswith("F") and len(move) == 2 and move[1] in "WASD":
                game.shoot_arrow(move[1])
            elif move in ["W", "A", "S", "D"]:
                game.move_player(move)
            else:
                print("Invalid input.")

        again = input("Play again? (Y/N): ").strip().upper()
        if again != 'Y':
            break

if __name__ == "__main__":
    main()
