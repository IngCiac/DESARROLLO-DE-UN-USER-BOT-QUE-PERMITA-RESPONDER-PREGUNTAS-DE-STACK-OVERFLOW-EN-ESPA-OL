import time
from app.database.connection import session
from app.database.schemas.question import Question
from app.libraries.chatbot import Chatbot
from app.database.connection import session,engine,Base
from telegram.ext import Updater,CommandHandler,MessageHandler,Filters
from nltk import SnowballStemmer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import logging

logger = logging.getLogger('mainlogger')
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('./app.log')
file_handler.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

def start(update, context):
    logger.debug('start command received')
    update.message.reply_text('Hola, soy un chatbot que te ayuda a hacer consultas de stackoverflow')
    update.message.reply_text('Preguntame lo que queiras sobre bases de datos mysqli que yo lo buscare en stackoverflow')

def help_command(update, context):
    logger.debug('help command received')
    update.message.reply_text('En que puedo ayudarte?')

def echo(update, context):
    try:
        #log message
        user_question = update.message.text.lower()
        logger.debug('\nmessage received ' + user_question)
        
        # Eliminar signos de puntuación y dividir la pregunta
        tokenizer = RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(user_question)
        print('Pregunta dividida: ' + str(tokens))    
        # Copiar el arreglo
        clean_tokens = tokens[:]
        # Eliminar palabras vacías: español => spanish
        stop_words = stopwords.words('spanish')
        for token in tokens:
            if token in stop_words:
                 clean_tokens.remove(token)
        print('Palabras vacías: ' + str(clean_tokens))        
        # Lematizar palabras
        spanish_stemmer = SnowballStemmer('spanish')
        stemmer_tokens = [spanish_stemmer.stem(token) for token in clean_tokens]
        print('Lematización: ' + str(stemmer_tokens))
        

        #quick responses
        if user_question in ('hola', 'buenas tardes', 'buenas noches'):
            return update.message.reply_text('Hola, que tal? en que te puedo ayudar')

        #load availabel responses
        
        questions_available = session.query(Question).all()
        logger.debug('questions available {questions_len} '.format(
            questions_len = len(questions_available)
        ))

        #create chatbot
        chatbot = Chatbot(questions = questions_available)
        database_question = chatbot.ask(user_question)
        logger.debug('database_question {database_question}'.format(database_question = database_question))

        #search response
        questions = session.query(Question).filter(Question.Title == database_question).all()
        logger.debug('questions match {questions_len} '.format(
            questions_len = len(questions)
        ))

        #if no response
        if len(questions) == 0:
            return update.message.reply_text('Lo siento, no tengo respuesta para esa pregunta :(')
        
        #response
        question = questions[0]
        logger.debug(str(question))
        update.message.reply_text('Creo que preguntaste: "{question}"'.format(question = database_question))
        print(len(question.Answer))
        update.message.reply_text(question.Answer[:500] + '...')
        update.message.reply_text('Puedes encontrar el post completo en')
        update.message.reply_text(question.Href)
    except Exception as error:
        logger.error(error)
        update.message.reply_text('Hay un bug en el bot y no puedo atenderte al momento, vuelve a intentarlo mas tarde')

def train_bot(file):
    logger.debug('creating bot')
    telegram_token = '1132143159:AAGNTkfjGd8_XNGueBis2qxQDi7Nzl0brlM'
    updater = Updater(
        token = telegram_token,
        use_context = True
    )
    dispatcher = updater.dispatcher
    logger.debug('command handler')
    dispatcher.add_handler(CommandHandler('start', start))
    #dispatcher.add_handler(CommandHandler("help", help_command))
    logger.debug('message handler')
    dispatcher.add_handler(MessageHandler(Filters.text, echo))

    logger.debug('start bot')
    updater.start_polling()
    logger.debug('bot started')

    logger.debug('bot idle')
    updater.idle()
    logger.debug('idle done')

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
    train_bot(file)
