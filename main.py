import json
import logging
import os

from dotenv import load_dotenv

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

from signal_api import Message, SignalAPI

load_dotenv()

logger = logging.getLogger(__name__)

async def message_handler(message: Message) -> None:
    day_folder_path = 'messages/' + message.time.strftime('%Y-%m-%d')
    day_folder_exists = os.path.exists(day_folder_path)

    if not day_folder_exists:
        os.makedirs(day_folder_path)
        logger.info('Created day messages folder.')

    with open(day_folder_path + '/' + str(message._timestamp) + '.json', 'w') as f:
        json.dump(message.data, f)
        logger.info('Saved message from: ' + message.sender_number)


def main():
    client = SignalAPI(os.environ["PHONE_NUMBER"], message_handler)
    logger.info("Starting...")
    client.run()


if __name__ == "__main__":
    main()
