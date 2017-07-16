#!/usr/bin/env python
import asyncio
import logging
from random import randint, random
import telepot
from telepot.aio.helper import ChatHandler

import os
from pymongo import MongoClient


class BigC(ChatHandler):
    def __init__(self,  *args, **kwargs):
        super(BigC, self).__init__(*args, **kwargs)
        self.uri = os.environ.get('DB_URI')
        self.client = MongoClient(self.uri)
        self.db = self.client['telegram-bigc']
        self.phrases = self.db['sentences']
        self.list_senteces = [x['sentence'] for x in self.phrases.find({})]
        self.got_list = False
        self.rate_num = 50.0

    async def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        if 'entities' in msg.keys():
            if msg['entities'][0]['type'] == 'bot_command':
                message = self.command_handler(msg, chat_id)
                await self.sender.sendMessage(message)
                return

        rate = self.rate_num/100.0
        rng = random()
        if content_type == 'text' and rng < rate:
            message = self.list_senteces[randint(1, len(self.list_senteces)-1)] \
                .format(msg['from']['first_name'])
            logging.info('Content type:{}::Chat type:{}::Chat Id:{}::Message:{}'.format(content_type, chat_type, chat_id, message))
            await self.sender.sendMessage(message)
        return


    def command_set_rate(self, command, chat_id):
        command_splited = command['text'].split()
        try:
            num = int(command_splited[1])
            if num > 0 and num < 100:
                # Salvar ID do grupo e salva a % de ativar o bot
                self.rate_num = num
                t_tele = 'Hum hum à {}%'.format(self.rate_num)
            else:
                raise ValueError
        except ValueError:
            t_tele = "Mas Sr. {0}, tem que ser um número entre 1 e 99".format(
                command['from']['first_name'])
        except IndexError:
            t_tele = "Mas Sr. {0}, tem que ser um número entre 1 e 99".format(
                    command['from']['first_name'])
        return t_tele

    def command_handler(self, msg, chat_id):
        command_splited = msg['text'].split()
        logging.info('Msg:{}::ChatId:{}'.format(command_splited[0], chat_id))

        if "/chance" in command_splited[0]:
            return self.command_set_rate(msg, chat_id)
        if "/status" in command_splited[0]:
            return "Nível de hum hum a {0}%".format(self.rate_num)
        if "/ajuda" in command_splited[0]:
            return "Normal {0}".format(msg['from']['first_name'])
