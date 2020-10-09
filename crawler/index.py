import time
from app.database.connection import session
from app.libraries.stackoverflow import StackOverflow
from app.libraries.chatbot import Chatbot
from app.database.connection import session, engine, Base
import logging

logger = logging.getLogger('mainlogger')
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('./app.log')
file_handler.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

def get_questions(file):
    stackoverflow: StackOverflow = StackOverflow()
    page = 1
    while True:
        stackoverflow.get_questions(page = page, file = file)
        page += 1

def train_bot(file):
    chatbot = Chatbot(file = file)
    response = chatbot.ask('crear una página de videos')
    print(response)

if __name__ == '__main__':
    logger.debug('main')
    must_loop = True
    while must_loop:
        try:
            logger.debug('creating database')
            Base.metadata.create_all(engine)
            logger.debug('database created')
            must_loop = False
        except Exception as error:
            logger.error('error creating database')
            logger.error(error)
            time.sleep(5)

    file = './storage/questions.txt'
    get_questions(file = file)
