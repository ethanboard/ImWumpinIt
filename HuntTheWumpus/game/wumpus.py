import random

class Game:
    def __init__(self):
        self.rooms = {i: [((i+1)%20)+1, ((i+2)%20)+1] for i in range(1, 21)}
        self.player = random.randint(1, 20)
        self.wumpus = random.randint(1, 20)
        while self.wumpus == self.player:
            self.wumpus = random.randint(1, 20)

    def start(self):
        print("Welcome to Hunt the Wumpus!")
        while True:
            print(f"You are in room {self.player}")
            if self.player == self.wumpus:
                print("You got eaten by the Wumpus. Yum.")
                break
            move = input("Enter a room number to move: ")
            try:
                move = int(move)
                if move in self.rooms[self.player]:
                    self.player = move
                else:
                    print("You can't move there.")
            except ValueError:
                print("Invalid input.")

if __name__ == "__main__":
    game = Game()
    game.start()