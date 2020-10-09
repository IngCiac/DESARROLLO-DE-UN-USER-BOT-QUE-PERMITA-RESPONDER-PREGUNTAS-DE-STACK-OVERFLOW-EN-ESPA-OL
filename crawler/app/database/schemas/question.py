import sqlalchemy
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from ..connection import Base

class Question(Base):
    __tablename__ = 'Question'

    Id = sqlalchemy.Column(sqlalchemy.Integer, nullable = False, primary_key = True)

    Title = sqlalchemy.Column(sqlalchemy.String, nullable = False)
    Href = sqlalchemy.Column(sqlalchemy.String, nullable = False)
    ShortDescription = sqlalchemy.Column(sqlalchemy.String, nullable = False)
    Content = sqlalchemy.Column(sqlalchemy.String, nullable = True)
    Answer = sqlalchemy.Column(sqlalchemy.String, nullable = True)
    CreatedAt = sqlalchemy.Column(sqlalchemy.DateTime, nullable = False, default = datetime.utcnow)

    def __str__(self):
        return str({
            'Id': self.Id,
            'Title': self.Title,
            'Href': self.Href,
            'ShortDescription': self.ShortDescription,
            'Content': self.Content,
            'Answer': self.Answer,
            'CreatedAt': self.CreatedAt
        })
