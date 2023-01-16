from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()


class Tool(db.Model):
    """
    Class that represents a software tool

    The following attributes of a software tool are stored in this table:
        * id - identificator of software tool
        * name - email address of the user
        * link - website of software tool
        * description - information about main functionalities of tool

    """
    __tablename__ = 'tool'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)
    link = db.Column(db.String(250))
    description = db.Column(db.String(500))

    def __init__(self, name: str, link: str, description: str):
        """Create a new Tool object using the name, link, description
        """
        self.name = name
        self.link = link
        self.description = description

    def __str__(self):
        return self.name


class Review(db.Model):
    """
    Class that represents a user review of particular software tool

    The following attributes of a review are stored in this table:
        * id -  identificator of review
        * tool_id - foreign key - id of tool
        * user_name - name of user creating a review
        * rating - rate of tool given by user
        * review_text - textural comment of user about the tool
        * review_date - date of review creation

    """
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tool_id = db.Column(db.Integer, db.ForeignKey('tool.id', ondelete="CASCADE"))
    user_name = db.Column(db.String(50))
    rating = db.Column(db.Integer)
    review_text = db.Column(db.String(500))
    review_date = db.Column(db.DateTime)

    @validates('rating')
    def validate_rating(self, key, value):
        assert value is None or (1 <= value <= 5)
        return value

    def __init__(self, tool_id: str, user_name: str, rating: int, review_text: str):
        """Create a new Review object using the tool id, user_name, given rating review text
        """
        self.tool_id = tool_id
        self.user_name = user_name
        self.rating = int(rating)
        self.review_text = review_text
        self.review_date = datetime.now()

    def __str__(self):
        return self.tool.name + " (" + self.review_date.strftime("%x") +")"
