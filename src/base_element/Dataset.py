
from torch.utils.data import Dataset

# 存放当前回合的信息
class CTurn:
    def __init__(self, role, obs_z, obs_x_no_action, obs_action, target):
        self.done = False  # 是否结束
        self.episode_return = 0.0  # 当前回合的累计奖励
        self.target = target  # 目标值（如胜负结果）
        self.obs_x_no_action = obs_x_no_action  # 当前状态的特征（不包含动作信息）
        self.obs_action = obs_action  # 当前动作的特征（如 one-hot 编码的出牌）
        self.obs_z = obs_z  # 历史信息（如前几轮的状态和动作序列）
        self.role = role  # 玩家角色（地主、农民1、农民2

class CDataset(Dataset):
    """可直接被 DataLoader 使用的轨迹数据集。"""

    def __init__(self, listPlays : list[list[CTurn]]):
        self.listPlays = listPlays
        self.done = []
        self.episode_return = []
        self.target = []
        self.obs_x_no_action = []
        self.obs_action = []
        self.obs_z = []
        
        for play in listPlays:
            for turn in play:
                self.done.append(turn.done)
                self.episode_return.append(turn.episode_return)
                self.target.append(turn.target)
                self.obs_x_no_action.append(turn.obs_x_no_action)
                self.obs_action.append(turn.obs_action)
                self.obs_z.append(turn.obs_z)

    def __len__(self):
        return len(self.target)

    def __getitem__(self, idx):
        return {
            "done": self.done[idx],
            "episode_return": self.episode_return[idx],
            "target": self.target[idx],
            "obs_x_no_action": self.obs_x_no_action[idx],
            "obs_action": self.obs_action[idx],
            "obs_z": self.obs_z[idx],
        }