#Fortnite.py
#Fortniteのシミュレーションを行うプログラム
#player 0 が n 回の試行で何回勝てるかを計測

import numpy as np
import math
import random
import matplotlib.pyplot as plt

n = 1000  #ゲームの試行回数
N = 100 #バトルロイヤルの人数
my_bias = 1.50 #自分自身のバイアス
victory_times = 0 #自分自身の勝利回数

def func_ramda(t):
    return 3 / 10 + 1 / (math.log(t-0.9) + t)

def func_E_me(h):
    #return 0.8
    return 1.05**(-h)

def func_E(h):
    return 1.03**(-float(h))

def func_G():
    random_number = random.random()

    if 0 <= random_number < 0.3:
        get_resource = 0
    if 0.3 <= random_number < 0.6:
        get_resource = 3
    elif 0.6 <= random_number < 0.9:
        get_resource = 4
    else:
        get_resource = 7

    return get_resource     

def bias(my_bias):
    for i in range(N):
        player_bias[i] = random.uniform(0.75, 1.50)
    player_bias[0] = my_bias

for x in range(n):
    t = 0                           #時間ステップ
    alive_list = [1] * N            #各プレイヤーが生存しているかを表すリスト
    combat_power_list = [0] * N     #各プレイヤーの戦闘力を表すリスト
    play_combat = []                #戦闘を行う人を格納するリスト
    alive_number = N                #生存人数の初期化
    serach_resource_list = [0] * N  #各プレイヤーが資源を探そうとしたかを表すリスト
    player_bias = [0] * N           #各プレイヤーのゲームの上手さでバイアスをかける

    #グラフ描画の変数
    t_list = []
    alive_number_list = []

    #初期状態を格納
    t_list.append(t)
    alive_number_list.append(alive_number)

    #バイアスの初期状態を格納
    bias(my_bias)

    while True:
        t = t + 1
        for i in range(N):
            serach_resource_list[i] = 0
        #print("t:",t)
        #各プレイヤーが資源を探すか判断する
        for i in range(N):
            if i == 0:
                decision_good = func_E(combat_power_list[i])
                random_number = random.random()

                if random_number < decision_good and combat_power_list[i] <= 100:
                    serach_resource_list[i] = 1
                    reward = func_G()
                    combat_power_list[i] += reward

            else:
                decision_good = func_E(combat_power_list[i])
                random_number = random.random()

                if random_number < decision_good and combat_power_list[i] <= 100:
                    serach_resource_list[i] = 1
                    reward = func_G()
                    combat_power_list[i] += reward

        #各プレイヤーが他のプレイヤーと出会うか判断する
        play_combat.clear() #初期化
        #print(play_combat)
        for i in range(N):
            meet_probability = func_ramda(t)
            if serach_resource_list[i] == 1:
                meet_probability += 0.1     #資源を探そうとしたプレイヤーに対してバイアスを加える
            random_number = random.random()

            if random_number < meet_probability:
                #print(i)
                play_combat.append(i)
                #print(play_combat)
        #print(play_combat)
        #戦闘を行う組み合わせを決める
        if len(play_combat) > 0:
            while True:
                #print(play_combat)
                player_a = random.choice(play_combat)
                play_combat.remove(player_a)

                player_b = random.choice(play_combat)
                play_combat.remove(player_b)     

                #戦闘が行われる
                power_a = player_bias[player_a] * combat_power_list[player_a]
                power_b = player_bias[player_b] * combat_power_list[player_b]
                
                if power_a < power_b:
                    reward = func_G()
                    alive_list[player_a] = 0
                    combat_power_list[player_b] += reward
                
                elif power_a > power_b:
                    reward
                    alive_list[player_b] = 0
                    combat_power_list[player_a] += reward
                
                else:
                    alive_list[player_a] = 0
                    alive_list[player_b] = 0
                #print(play_combat)
                #残り1人になったら生き残るものとする
                if len(play_combat) < 2:
                    break

        #生存人数を数える
        alive_number = 0
        for item in alive_list:
            if item == 1:
                alive_number += 1
        
        #グラフ描画のためにリストに代入
        t_list.append(t)
        alive_number_list.append(alive_number)

        #生存人数が一人かどうか確認
        if alive_number <= 1:
            break

        
        #自分自身が脱落したら強制終了
        if alive_list[0] == 0:
            break
        
    #print(combat_power_list)    
    if alive_number == 1:
        for i in range(N):
            if alive_list[i] == 1:
                print("Winner is player",i)
                #print("player {0}'s power is {1}".format(i,combat_power_list[i]))
    else:
        print("Winner is none or I lose")

    #自分自身が何回勝利したかを記録
    if alive_list[0] == 1:
        victory_times += 1

print("victory times is",victory_times)

"""
#グラフ描画
t_list = np.arange(0, max(t_list) + 1, 1) #グラフ描画のために整形
plt.xlabel("Time")
plt.ylabel("Survival number of people")
plt.ylim([0, N])
plt.plot(t_list,alive_number_list)
plt.show()
"""