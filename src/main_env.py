listPlayer = [RandomPlayer(), RandomPlayer(), RandomPlayer()]
game = Game("sandbox", listPlayer)
state = game.reset()
while game.is_running():
    action = input("Enter your action: ")
    state, reward, done, info = game.step(action)
    print(f"State: {state}, Reward: {reward}, Done: {done}, Info: {info}")