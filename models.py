from exts import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    telephone = db.Column(db.String(11), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    # now()方法表示的是服务器第一次运行的时间
    # now方法表示每次创建一个模型的时候，都获取当前的时间
    create_time = db.Column(db.DateTime, default=datetime.now)
    # 外键的映射
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    answer_num = db.Column(db.Integer, nullable=False)
    author = db.relationship('User', backref=db.backref('questions'))

class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    #desc降序排列,通过自身id
    question = db.relationship('Question', backref=db.backref('answers', order_by=id.desc()))
    author = db.relationship('User', backref=db.backref('answers'))