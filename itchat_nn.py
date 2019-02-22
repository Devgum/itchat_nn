# coding:utf-8

import sys

import itchat
from nn_rule import *
from itchat.content import *
from itchat.storage import User, Chatroom

pkl_file = 'itchat.pkl'
games = {}


def get_names(msg):
    '''
    获取信息所属会话名称和信息属主昵称
    '''
    msg_user = msg['User']
    if isinstance(msg_user, User):
        # 单人会话，会话名即用户昵称
        nick_name = msg_user['NickName']
        contact_name = nick_name
        return nick_name, contact_name

    # 多人会话，获取用户昵称
    if 'ActualNickName' in msg and msg['ActualNickName']:
        nick_name = msg['ActualNickName']
    else:
        msg_user = itchat.update_chatroom(msg_user['UserName'])
        from_user = msg_user.search_member(userName=msg['FromUserName'])
        nick_name = from_user['NickName']

    # 多人会话，获取会话名
    if 'NickName' in msg_user:
        contact_name = msg_user['NickName']
    else:
        msg_user = itchat.update_chatroom(msg_user['UserName'])
        contact_name = msg_user['NickName']
    return nick_name, contact_name


def create_game(msg):
    '''
    监听游戏创建
    '''
    msg_content = msg['Content']
    if msg_content == '.新建':
        msg_user = msg['User']
        nick_name, contact_name = get_names(msg)
        if contact_name in games:
            msg_user.send('游戏已存在, 回复".报名"参加游戏, 或回复".结束"结束游戏')
            return True
        games[contact_name] = NNGame()
        # 如果是单人会话，直接添加双方为玩家
        if isinstance(msg_user, User):
            from_user = itchat.update_friend(msg['FromUserName'])
            player1 = Player(from_user['NickName'])
            player2 = Player(nick_name)
            games[contact_name].add_player(player1)
            games[contact_name].add_player(player2)
            msg_user.send(f'新游戏已创建, 请庄家[{player1.name}]发牌')
        else:
            msg_user.send('新游戏已创建, 回复".报名"参加游戏')
        return True
    return False


def enter_game(msg):
    '''
    监听报名
    '''
    msg_content = msg['Content']
    if msg_content == '.报名':
        msg_user = msg['User']
        if isinstance(msg_user, User):
            return True
        nick_name, contact_name = get_names(msg)
        if contact_name not in games:
            msg_user.send(
                '当前会话中没有正在进行的游戏，回复".新建"创建新游戏')
            return True
        game = games[contact_name]
        if game.player_exists(nick_name):
            msg_user.send(f'玩家{nick_name}已经存在，不需要重复报名')
            return True
        player = Player(nick_name)
        game.add_player(player)
        msg_user.send(
            f'已添加玩家[{nick_name}]，目前玩家数量[{game.count_players()}]')
        return True


def exit_game(msg):
    '''
    监听退出
    '''
    msg_content = msg['Content']
    if msg_content == '.退出':
        msg_user = msg['User']
        if isinstance(msg_user, User):
            return True
        nick_name, contact_name = get_names(msg)
        if contact_name not in games:
            msg_user.send(
                '当前会话中没有正在进行的游戏，回复".新建"创建新游戏')
            return True
        game = games[contact_name]
        if not game.player_exists(nick_name):
            msg_user.send(f'玩家{nick_name}未加入游戏，不需要退出')
            return True
        final_score = game.get_player(nick_name).score
        # TODO: 中途退出需要有惩罚机制
        game.del_player(nick_name)
        msg_user.send(f'玩家{nick_name}退出游戏，最终得分: {final_score}')
        return True
    return False


def run_game(msg):
    '''
    监听开始
    '''
    msg_content = msg['Content']
    if msg_content == '.开始' or msg_content == '.继续' or msg_content == '.发牌':
        msg_user = msg['User']
        nick_name, contact_name = get_names(msg)
        if contact_name not in games:
            msg_user.send(
                '当前会话中没有正在进行的游戏，回复".新建"创建新游戏')
            return True
        game = games[contact_name]
        if isinstance(msg_user, User):
            from_user = itchat.update_friend(msg['FromUserName'])
            nick_name = from_user['NickName']
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
        result = f'{game.display_stat()}\n{game.count_score()}\n'
        msg_user.send(result)
        game.reset()
        return True
    return False


def end_game(msg):
    '''
    监听结束
    '''
    msg_content = msg['Content']
    if msg_content == '.结束':
        msg_user = msg['User']
        nick_name, contact_name = get_names(msg)
        if contact_name not in games:
            msg_user.send(
                '当前会话中没有正在进行的游戏，回复".新建"创建新游戏')
            return True
        del games[contact_name]
        msg_user.send('游戏结束')
        return True
    return False


@itchat.msg_register(TEXT, isFriendChat=True, isGroupChat=True)
def text_reply(msg):
    reply_funcs = [create_game, enter_game, exit_game, run_game, end_game]
    for reply_func in reply_funcs:
        if reply_func(msg):
            return


cmdQR = 2
if len(sys.argv) > 1:
    cmdQR = sys.argv[1]
itchat.auto_login(hotReload=True, enableCmdQR=cmdQR, statusStorageDir=pkl_file)
itchat.run()
