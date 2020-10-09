import requests
import bs4
import datetime
from app.database.schemas.question import Question
from app.database.connection import session
import logging
import codecs

logger = logging.getLogger('mainlogger')


class StackOverflow:
    def __init__(self, base_url = 'https://es.stackoverflow.com'):
        self.base_url = base_url
    
    def get_questions(self, page = 1, file = 'questions.txt'):
        url = '{base_url}/questions/tagged/mysqli?page={page}&sort=votes&pagesize=50'.format(
            base_url = self.base_url,
            page = page
        )
        logger.debug('looking question for url ' + url)
        questions_response = requests.get(url)
        questions_page = bs4.BeautifulSoup(questions_response.content, 'html.parser')
        divs = questions_page.find_all('div', attrs = { 'class': 'question-summary' })
        divs_len = len(divs)
        for index, question_summary in enumerate(divs):
            logger.debug('question {index}/{divs_len}'.format(index = index, divs_len = divs_len))
            question_hyperlink = question_summary.find('a', attrs = { 'class': 'question-hyperlink' })
            excerpt = question_summary.find('div', attrs = { 'class': 'excerpt' })
            
            href = self.base_url + question_hyperlink['href']
            title = question_hyperlink.getText()
            short_description = excerpt.getText()

            if session.query(Question)\
                .filter(
                    Question.Title == title,
                    Question.Href == href,
                    Question.ShortDescription == short_description
                )\
                .count() == 0:

                logger.debug('looking for response url ' + href)

                responses_response = requests.get(href)
                responses_page = bs4.BeautifulSoup(responses_response.content, 'html.parser')
                
                content = responses_page.find('div', class_ = 'post-text').text
                answer1 = responses_page.find('div', class_ = 'answercell')
                answer = answer1.find('div' , class_ = 'post-text').text
                #title = div.find('a').text

                question = Question(
                    Title = title,
                    Href = href,
                    ShortDescription = short_description,
                    Content = content,
                    Answer = answer
                )
                session.add(question)
                session.commit()

                with codecs.open('questions.txt', 'a', 'utf-8') as file:
                    file.write(title + '\n')
