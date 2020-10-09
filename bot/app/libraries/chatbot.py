import pandas
import codecs
from math import *
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import logging
import datetime

logger = logging.getLogger('mainlogger')

class Chatbot:
    def __init__(self, questions):
        '''
        questions = []
        with codecs.open(file, 'r', 'utf-8') as f:
            for line in f:
                questions.append(line)

        status = []
        for i in range(len(questions)):
            status.append(i)
        self.__data = {
            'text': questions,
            'status': status
        }
        '''

        questions_text = []
        for question in questions:
            questions_text.append(question.Title)

        status = []
        for i in range(len(questions_text)):
            status.append(i)

        self.__data = {
            'text': questions_text,
            'status': status
        }

    def frame(self):
        frame = pandas.DataFrame(self.__data)
        self.frame_x = frame['text']
        self.frame_y = frame['status']

    def learning(self):
        self.vect = TfidfVectorizer(min_df=1)
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.frame_x, self.frame_y, test_size = 0.2, random_state = 4)
        self.x_trainvect = self.vect.fit_transform(self.x_train)
        self.x_trainvect.toarray()
        self.vect1 = TfidfVectorizer(min_df = 1)
        self.x_trainvect = self.vect1.fit_transform(self.x_train)
        a = self.x_trainvect.toarray()
        self.vect1.inverse_transform(a[0])

    def bayes(self):
        self.mnb = MultinomialNB()
        self.y_train=self.y_train.astype('int')
        self.mnb.fit(self.x_trainvect,self.y_train)

    def ask(self, sentence):
        logger.debug('ask to bot for: {question}'.format(question = sentence))
        start = datetime.datetime.now()
        self.frame()
        self.learning()
        self.bayes()
        x_testvect = self.vect1.transform([sentence])
        pred = self.mnb.predict(x_testvect)
        end = datetime.datetime.now()
        logger.debug('time elapsed {time}'.format(time = end - start))
        return self.frame_x[pred[0]]
