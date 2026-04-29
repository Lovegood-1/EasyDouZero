listPlayer = [RandomPlayer(), RandomPlayer(), RandomPlayer()]
game = Game("sandbox", listPlayer)
state = game.reset()
while game.is_running():
    action = input("Enter your action: ")
    state, done = game.step(action)
    print(f"State: {state}, Done: {done}")