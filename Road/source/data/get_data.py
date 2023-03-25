from telethon import TelegramClient, events
import csv

api_id = 28394694
api_hash = "4c0b02c61f2626bd3f0d1b58883ec759"
client = TelegramClient(
    "session_name", api_id, api_hash
)  # create a client object to connect to telegram using my account info
client.start()


@client.on(
    events.NewMessage(chats="AhwalTareq")
)  # create event handler to listen to AhwalTareq for new messages
async def my_event_handler(event) -> None:
    """this function get called by the event handler
    when we recive new message from AhwalTareq group

    Args:
        event : the payload from telegram server contain the information about the new message
    """
    with open("data.csv", "a+", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(
            csvfile, fieldnames=event.message.to_dict().keys()
        )  # init a csv writer
        writer.writerow(
            event.message.to_dict()
        )  # write the message with its meta data to the file


# Runs the event loop until the library is disconnected.
client.run_until_disconnected()
