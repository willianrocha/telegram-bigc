#!/usr/bin/env python
import asyncio
import logging
from random import randint, random
import telepot
from telepot.aio.helper import ChatHandler

class BigC(ChatHandler):
    def __init__(self,  *args, **kwargs):
        super(BigC, self).__init__(*args, **kwargs)

        self.list_senteces = ["mas deixe","hum hum","ai ai", "é mesmo é?", "como é que é \
        o negócio?", "como é que é essa história?","ô que vida, ein?", "Eita",
        "Será o Bené?", "Que pozinho é esse?", "de repente, não mais que de repente",
        "como é que é essa história {0}?","que foi que tu disse {0}?",
        "Tudo bem, moça?", "Fale Sr. {0}", "E ai Sr. {0}",
        "Mas, e ai Sr. {0}, conte uma nova",  "Top de linda", "Miau Gatinha"]
        self.rate_num = 50.0
        # self._answer = random.randint(0,99)

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
            logging.info('Content type: {} :: Chat type: {} :: Chat Id:{}'.format(content_type, chat_type, chat_id))
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
        logging.info('Msg: {} ::Chat Id:{}'.format(msg, chat_id))

        if "/chance" in command_splited[0]:
            return self.command_set_rate(msg, chat_id)
        if "/status" in command_splited[0]:
            return "Nível de hum hum a {0}%".format(self.rate_num)
        if "/ajuda" in command_splited[0]:
            return "Normal {0}".format(msg['from']['first_name'])
