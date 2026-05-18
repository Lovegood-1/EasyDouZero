from src.base_element.Dataset import CDataset, CTurn
from src.Env import CEnv

def collect_dataset(env, num_plays=1000, model_dict=None):
    listPlays = []
    for episode in range(num_plays):
        print(f"正在收集第 {episode+1}/{num_plays} 局游戏数据...")
        listTurns = collect_single_play(model_dict=model_dict)
        listPlays.append(listTurns)
    dataset = CDataset(listPlays)
    return dataset

# 运行一局游戏，收集游戏记录数据
def collect_single_play(model_dict=None):
    listTurns = []
    game = CEnv(mode=CGameMode.SANDBOX, players=build_random_players())
    game.play_start() # 发牌等初始化步骤
    turn = game.get_turn()
    listTurns.append(turn)
    while not game.play_end():
        for role, player in game.players.items():
            print(f"玩家 {role} 的手牌: {player.hand_cards}")
        # 打印 game records
        print(f"游戏记录: {game.record}")
        # actions = game.cur_legal_actions()
        # action = game.players[game.current_player].agent.select_action(actions)  # 这里假设玩家对象有一个 agent 属性，agent 有一个 select_action 方法
        model = model_dict[game.current_player] if model_dict else None
        with torch.no_grad():
            action = model.forward(turn)
        print(f"当前玩家: {game.current_player}, 出牌: {action}")
        game.play_step(action)
        turn = game.get_turn()
        listTurns.append(turn)
    return listTurns