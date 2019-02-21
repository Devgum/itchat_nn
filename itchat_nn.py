# coding:utf-8

import sys

import itchat
from nn_rule import *
from itchat.content import *
from itchat.storage import User, Chatroom

pkl_file = 'itchat.pkl'
games = {}


def get_names(msg):
    msg_user = msg['User']
    if isinstance(msg_user, User):
        nick_name = msg_user['NickName']
        contact_name = nick_name
    else:
        if 'ActualNickName' in msg:
            nick_name = msg['ActualNickName']
        else:
            from_user = itchat.update_friend(msg['ActualUserName'])
            nick_name = from_user['NickName']
        if 'NickName' in msg_user:
            contact_name = msg_user['NickName']
        else:
            chatroom = itchat.update_chatroom(msg_user['UserName'])
            contact_name = chatroom['NickName']
    return nick_name, contact_name


@itchat.msg_register(TEXT, isFriendChat=True, isGroupChat=True)
def text_reply(msg):
    msg_content = msg['Content']
    msg_user = msg['User']
    nick_name, contact_name = get_names(msg)
    if isinstance(msg_user, User):
        return
    if isinstance(msg_user, Chatroom):
        if msg_content == '.新建':
            games[contact_name] = NNGame()
            msg_user.send('新游戏已创建')
            return
        if msg_content == '.报名':
            if contact_name in games:
                if not nick_name:
                    msg_user.send('无法获取玩家昵称，请重新尝试报名')
                    return
                game = games[contact_name]
                if game.player_exists(nick_name):
                    return
                player = Player(nick_name)
                game.add_player(player)
                msg_user.send(
                    f'已添加玩家[{nick_name}]，目前玩家数量[{game.count_players()}]')
                return
        if msg_content == '.退出':
            if contact_name in games:
                game = games[contact_name]
                if not game.player_exists(nick_name):
                    game.del_player(nick_name)
        if msg_content == '.开始' or msg_content == '.继续' or msg_content == '.发牌':
            if contact_name in games:
                game = games[contact_name]
                if game.master_player().name != nick_name:
                    msg_user.send(f'只能由庄家[{game.master_player().name}]发牌')
                    return
                if game.count_players() < 2:
                    msg_user.send(f'人数不够')
                    return
                if game.count_players() > 10:
                    msg_user.send(f'人数过多')
                    return
                for i in range(5):
                    game.draw()
                game.count_nn()
                result = ''
                result += f'{game.display_stat()}\n'
                result += f'{game.count_score()}\n'
                game.reset()
                msg_user.send(result)
                return
        if msg_content == '.结束':
            if contact_name in games:
                del games[contact_name]
                msg_user.send('游戏结束')

cmdQR = 2
if len(sys.argv) > 1:
    cmdQR = sys.argv[1]
itchat.auto_login(hotReload=True, enableCmdQR=cmdQR, statusStorageDir=pkl_file)
itchat.run()
