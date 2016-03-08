from uuid import uuid4
import logging

from game import Game
from player import Player

LINK_PATTERN = 'https://telegram.me/%s?start=%s'


class GameManager(object):
    """ Manages all running games by using a confusing amount of dicts """

    def __init__(self):
        self.gameid_game = dict()
        self.userid_game = dict()
        self.chatid_gameid = dict()  # Goes both ways
        self.userid_player = dict()
        self.logger = logging.getLogger(__name__)

    def generate_invite_link(self, bot_name, chat_id):
        """
        Generate a game join link with a unique ID and connect the game to the
        group chat
        """
        game_id = str(uuid4())
        game = Game()

        self.logger.info("Creating new game with id " + game_id)
        self.gameid_game[game_id] = game
        self.chatid_gameid[chat_id] = game_id
        self.chatid_gameid[game_id] = chat_id
        self.chatid_gameid[game] = chat_id

        return LINK_PATTERN % (bot_name, game_id)

    def join_game(self, game_id, user):
        """ Create a player from the Telegram user and add it to the game """
        self.logger.info("Joining game with id " + game_id)
        game = self.gameid_game[game_id]
        player = Player(game, user)
        self.userid_player[user.id] = player
        self.userid_game[user.id] = game

    def leave_game(self, user):
        """ Remove a player from its current game """
        player = self.userid_player[user.id]

        player.leave()
        del self.userid_player[user.id]
        del self.userid_game[user.id]

