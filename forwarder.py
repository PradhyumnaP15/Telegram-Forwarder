from telethon import TelegramClient, events, sync
from telethon.tl.patched import MessageService
from dotenv import load_dotenv
import os
import yaml
import logging
import sys
import asyncio

api_id: 2847976
api_hash: 55e25e81f54f33fec14f12faa9964554
    
load_dotenv()
API_ID = os.getenv('api_id')
API_HASH = os.getenv('api_hash')
SESSION_NAME = os.getenv('session_name')

assert API_ID and API_HASH and SESSION_NAME

def forwarder():
    print(config)
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    client.start()

    confirm = ''' 
            IMPORTANT 🛑
            Are you sure You want to START FORWARDING MESSAGES?
            Kindly Confirm your Source Chats and Target Chats.

            Press [ENTER] to continue:
            '''

    input(confirm)

    SOURCE_CHATS = []
    TARGET_CHATS = []
    for dialog in client.iter_dialogs():
        if dialog.name in config["your_source_chats"]:
            SOURCE_CHATS.append(dialog.entity.id)
        if dialog.name in config["your_target_chats"]:
            TARGET_CHATS.append(dialog.entity.id)

    if not TARGET_CHATS:
        logging.info(f"Could not find any matching target chat in the user's dialogs")
        sys.exit(1)

    if not SOURCE_CHATS:
        logging.info(f"Could not find any matching source in the user's dialogs")
        sys.exit(1)

    logging.info(f"Listening on {len(SOURCE_CHATS)} channels. Forwarding messages to {len(TARGET_CHATS)} channels.")

    print('\nProgram Started! Event Handler Waiting for messages to forward!\n')
    
    @client.on(events.NewMessage(chats= SOURCE_CHATS))
    async def handler(event):
        last_sender = None
        for target in TARGET_CHATS:
            # await client.forward_messages(output_channel, event.message)
            message_with_from_header = event.message
            sender = await event.message.get_sender()
            if sender.first_name:
                first_name = sender.first_name
            else:
                first_name = ''
            if sender.last_name:
                last_name = sender.last_name
            else:
                last_name = ''
            
            if sender != last_sender:
                message_with_from_header.text = '`✉️ From: `'+'**'+first_name+'** '+'**'+last_name+'**'+'\n\n' + message_with_from_header.text
            else:
                pass

            await client.send_message(target, message_with_from_header)
            last_sender = sender
            print('Message forwarded Successfully! From Soucrce Chats to Target Chats | Message id:',event.message.id)
            print('Program Running (Event Handler Waiting for more Messages).....')

    client.run_until_disconnected()

if __name__ == "__main__":
    with open('config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)
        forwarder()
    
