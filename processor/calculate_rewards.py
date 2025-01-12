import json 
from utils import ROLE2FEATURE, ACTION2FEATURE
import numpy as np
import re

def reverse_dict(d):
    new_dict = {}
    for key, value in d.items():
        if value not in new_dict:
            new_dict[value] = key
        else:
            new_dict[value] += '/' + key
    return new_dict
def format_round(text):
    formatted_text = re.sub(
    r'(is speaking)\(Round (\d+)\)',  # 匹配模式
    lambda match: f"{match.group(1)} (round {match.group(2)})",  # 替换内容
    text
)
    return formatted_text
# FEATURE2CLASS = reverse_dict(CLASS2FEATURE)
FEATURE2ROLE = reverse_dict(ROLE2FEATURE)
FEATURE2ACTION = reverse_dict(ACTION2FEATURE)


def get_player_id(text):

    match = re.search(r'\[(\d+)\]', text)

    if match:
        number = match.group(1)  # 提取匹配的数字
        # print(f"Extracted number: {number}")
        return int(number)
    else:
        print("No number found in brackets.")
        return None

def load_data(path='./data_feature.json'):
    with open(path,mode='r',encoding='utf-8-sig') as f :
        game_data = json.load(f)
    return game_data
def save_data(path='data_feature_with_reward.json',game_data=None):
    with open(path, 'w', encoding='utf-8-sig') as f:
        json.dump(game_data, f, indent=4, ensure_ascii=False)
def calculate_reward(data):
    
    for game_id in data.keys():
        game_state = data[game_id]['game_state']
        id2roles = game_state['roles']
        # print(f'id2roles = {id2roles}')
        roles2id = reverse_dict(id2roles)
    
        
        speed_tasks = data[game_id]['time_fine'].keys()
        for speed_task in speed_tasks:
            if "Round" in speed_task:
                speed_task = format_round(speed_task)
            reward  = 0
            play_id = get_player_id(speed_task)
            role    = id2roles[str(play_id)]
            feature = data[game_id]['audio'][speed_task]['feature'] 
            feature = np.array(feature).reshape(-1,2)
            if role in ["Werewolf"]:
                for index, (pred_other_role_id,pred_action_id) in enumerate(zip(feature[:,0],feature[:,1]) ):
                    index +=1
                    # if index == play_id:
                    #     continue
                    real_other_role = id2roles[str(index)]
                    if pred_other_role_id != 0:
                        pred_other_role_id -= 1
                        
                        ROLE_REWARD_MAPPING = {
                                    '预言家': 6,
                                    '女巫': 5,
                                    '村民': 3,
                                    '猎人': 4,
                                    '好人': 3,
                                    '神职': 6,
                                    '金水': 2,
                                    '银水': 2,
                                    '不确定身份': 1,
                                    '狼人': -6
                                }
                        if real_other_role == 'Seer':
                            pass 
                        elif real_other_role == 'Witch':
                            ROLE_REWARD_MAPPING['女巫'] = 6
                            ROLE_REWARD_MAPPING['预言家'] = 2
                            ROLE_REWARD_MAPPING['狼人'] = 0
                            pass 
                        elif real_other_role == 'Hunter':
                            ROLE_REWARD_MAPPING['狼人'] = 0
                            ROLE_REWARD_MAPPING['预言家'] = 2
                            ROLE_REWARD_MAPPING['猎人'] = 6
                            
                            pass 
                        elif real_other_role == 'Villager':
                            ROLE_REWARD_MAPPING['村民'] = 6
                            ROLE_REWARD_MAPPING['猎人'] = 2
                            ROLE_REWARD_MAPPING['狼人'] = 4
                            
                            pass 
                        else:   
                            
                            pass
                        reward+= ROLE_REWARD_MAPPING[FEATURE2ROLE[pred_other_role_id]]
                    if pred_action_id !=0:
                        pred_action_id -= 1
                        
                        if real_other_role == 'Werewolf':
                            Action_REWARD_MAPPING = {                                       
                                        '查验': -10,
                                        '救': 6,
                                        '毒': -6,
                                        '开枪': -6,
                                        '刀口': -4,
                                        '自爆': -10,
                                        '投票': -6,
                                    }
                            pass 
                        else:   
                            Action_REWARD_MAPPING = {                                       
                                        '查验': 10,
                                        '救': -6,
                                        '毒': 6,
                                        '开枪': 6,
                                        '刀口': 4,
                                        '自爆': -20,
                                        '投票': 6,
                                    }
                            pass
                        reward+= Action_REWARD_MAPPING[FEATURE2ACTION[pred_action_id]]
                pass 
            else:
                for index, (pred_other_role_id,pred_action_id) in enumerate(zip(feature[:,0],feature[:,1]) ):
                    index +=1
                    # if index == play_id:
                    #     continue
                    real_other_role = id2roles[str(index)]
                    if pred_other_role_id != 0:
                        pred_other_role_id -= 1
                        
                        ROLE_REWARD_MAPPING = {
                                    '预言家': 6,
                                    '女巫': 0,
                                    '村民': 0,
                                    '猎人': 0,
                                    '好人': 1,
                                    '神职': 5,
                                    '金水': 6,
                                    '银水': 6,
                                    '不确定身份': 1,
                                    '狼人': -6
                                }
                        if real_other_role == 'Seer':
                            pass 
                        elif real_other_role == 'Witch':
                            ROLE_REWARD_MAPPING['女巫'] = 6
                            ROLE_REWARD_MAPPING['预言家'] = 0
                            ROLE_REWARD_MAPPING['狼人'] = -5
                            pass 
                        elif real_other_role == 'Hunter':
                            ROLE_REWARD_MAPPING['预言家'] = 0
                            
                            
                            ROLE_REWARD_MAPPING['猎人'] = 6
                            ROLE_REWARD_MAPPING['狼人'] = -4
                            
                            
                            pass 
                        elif real_other_role == 'Villager':
                            ROLE_REWARD_MAPPING['村民'] = 6
                            ROLE_REWARD_MAPPING['预言家'] = 0
                            ROLE_REWARD_MAPPING['狼人'] = -3
                            ROLE_REWARD_MAPPING['神职'] = 0

                            pass 
                        else: # werewolf
                            ROLE_REWARD_MAPPING['预言家'] = -6
                            ROLE_REWARD_MAPPING['女巫'] = -5
                            ROLE_REWARD_MAPPING['猎人'] = -4
                            ROLE_REWARD_MAPPING['村民'] = -3
                            ROLE_REWARD_MAPPING['金水'] = -6
                            ROLE_REWARD_MAPPING['银水'] = -6
                            ROLE_REWARD_MAPPING['狼人'] = 6
                            
                            
                            pass
                        reward+= ROLE_REWARD_MAPPING[FEATURE2ROLE[pred_other_role_id]]
                    if pred_action_id !=0:
                        pred_action_id -= 1
                        
                        if real_other_role == 'Werewolf':
                            Action_REWARD_MAPPING = {                                       
                                        '查验': 10,
                                        '救': -6,
                                        '毒': 6,
                                        '开枪': 6,
                                        '刀口': 4,
                                        '自爆': -10,
                                        '投票': 6,
                                    }
                            pass 
                        else:   
                            Action_REWARD_MAPPING = {                                       
                                        '查验': 4,
                                        '救': 6,
                                        '毒': -6,
                                        '开枪': -6,
                                        '刀口': -4,
                                        '自爆': -20,
                                        '投票': -6,
                                    }
                            pass
                        reward+= Action_REWARD_MAPPING[FEATURE2ACTION[pred_action_id]]
                # print(f'speak reward: {reward}')
                pass 
                pass 
            
            data[game_id]['audio'][speed_task]['reward'] = reward
    

game_data = load_data('./data_feature.json')
calculate_reward(game_data)
save_data('./data_feature_with_reward.json',game_data)
