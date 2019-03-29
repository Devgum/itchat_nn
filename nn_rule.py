# coding:utf-8

from player import Player
from poker import *

class NNGame:

    def __init__(self, base_score=10):
        self.pack = create_pack(with_joker=False)
        self.base_score = base_score
        self.master = ''
        self.players = {}

    def player_exists(self, player_name):
        return player_name in self.players

    def count_players(self):
        return len(self.players)

    def add_player(self, player):
        if not self.master:
            self.master = player.name
        self.players[player.name] = player

    def del_player(self, player_name):
        if player_name in self.players:
            if self.master == player_name:
                self.next_master()
            del self.players[player_name]

    def get_player(self, player_name):
        if player_name in self.players:
            return self.players[player_name]
        raise(f'Player [{player_name}] does not exist.')

    def master_player(self):
        return self.players[self.master]

    def reset(self):
        self.pack = create_pack(with_joker=False)
        for player in self.players.values():
            player.reset()

    def display_stat(self):
        result = ''
        for player_name in self.players:
            player = self.players[player_name]
            role = ''
            if self.master == player_name:
                role = '(庄家)'
            result += f'{player.name}{role}:\n'
            result += f'{player.display_hand()}\n'
        return result

    def draw(self):
        for player in self.players.values():
            player.draw(self.pack)

    def count_nn(self):
        for player in self.players.values():
            if len(player.hand) is not 5:
                print(
                    f'Player [{player.name}]: Hand size [{len(player.hand)}]')
                return
            values = []
            for card in player.hand:
                value = card.value + 1
                if value > 10:
                    value = 10
                values.append(value)
            nn = -1
            for i in range(3):
                for j in range(i + 1, 4):
                    for k in range(j + 1, 5):
                        s = values[i] + values[j] + values[k]
                        if s % 10 == 0:
                            nn = sum(values) % 10
                            if nn == 0:
                                nn = 10
                    else:
                        continue
                    break
                else:
                    continue
                break
            player.nn = nn

    def count_winner(self, nn):
        diff = self.base_score
        if nn == 0:
            diff *= 4
        elif nn > 7:
            diff *= nn - 6
        return diff

    def next_master(self):
        player_name_list = list(self.players.keys())
        master_index = player_name_list.index(self.master)
        new_index = (master_index + 1) % len(player_name_list)
        self.master = player_name_list[new_index]

    def display_nn(self, nn):
        if nn < 0:
            return '没牛'
        if nn == 10 or nn == 0:
            return '牛牛'
        return f'牛{nn}'

    def count_score(self):
        result = ''
        master_get = 0
        master = self.players[self.master]
        for player_name in self.players:
            if player_name == self.master:
                continue
            diff = self.base_score
            player = self.players[player_name]
            if player.nn < master.nn:
                diff = self.count_winner(master.nn)
            elif player.nn > master.nn:
                diff = 0 - self.count_winner(player.nn)
            else:
                if player.hand > master.hand:
                    diff = 0 - self.count_winner(player.nn)
                elif player.hand == master.hand:
                    diff = 0
                else:
                    diff = self.count_winner(master.nn)
            master_get += diff
            player.score -= diff
            result += f'{player.name} [{self.display_nn(player.nn)}] 本局: {0-diff}. 当前: {player.score}\n'
        self.players[self.master].score += master_get
        result += f'{master.name}(庄家) [{self.display_nn(master.nn)}] 本局: {master_get}. 当前: {master.score}\n'
        if master.nn < 0:
            self.next_master()
            result += f'\n庄家下庄, [{self.master_player().name}]坐庄\n'
        else:
            result += f'\n庄家有牛，[{self.master_player().name}]坐庄\n'
        return result


if __name__ == '__main__':
    game = NNGame()
    players = ['Mario', 'Luigi', 'Toadette', 'Toad']
    for player in players:
        game.add_player(Player(player, score=0))
    try:
        for i in range(5):
            game.draw()
        game.count_nn()
        print(game.display_stat())
        print(game.count_score())
        game.reset()
    except KeyboardInterrupt as e:
        print("KeyboardInterrupt")
