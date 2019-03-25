from flask import Flask, render_template, request, redirect, url_for, session
import config
from models import User, Question, Answer
from exts import db
from decorations import login_required
from sqlalchemy import or_

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    context = {
        'questions': Question.query.order_by('-create_time').all()
    }

    return render_template('index.html', **context)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter(User.username == username, User.password == password).first()
        if user:
            # 将用户相关信息保存到cookie中
            session['user_id'] = user.id
            #如果想在31天内都不需要登录
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return '用户名或密码错误！请核对后再试'
@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form.get('username')
        telephone = request.form.get('telephone')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #手机号码验证，如果被注册了，就不能再注册了
        tele = User.query.filter(User.telephone == telephone).first()
        user = User.query.filter(User.username == username).first()
        if tele:
            return '该手机号码已经被注册，请更换手机号码！'
        elif user:
            return '该用户名已被注册，请更换用户名！'
        else:
            # password1要与password2相等
            if password1 != password2:
                return '两次密码不正确，请核对后再试'
            else:
                user = User(username=username, telephone=telephone, password=password1)
                db.session.add(user)
                db.session.commit()
                # 如果注册成功，就让页面跳转到登陆的页面
                return redirect(url_for('login'))

@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            temp = {'user': user}
            return temp
    #这里必须要返回一个空字典，不然上述生成字典不可以在项目中使用
    return {}

@app.route('/logout/')
def logout():
    #session.pop('user_id')
    # del session('user_id')
    session.clear()
    return redirect(url_for('index'))

@app.route('/question/', methods=['GET', 'POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title, content=content)

        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        question.author = user

        db.session.add(question)
        db.session.commit()

        return redirect(url_for('index'))

@app.route('/detail/<question_id>/')
def detail(question_id):
    question_model = Question.query.filter(Question.id == question_id).first()
    temp1 = Answer.query.count()

    question.answer_num = temp1
    # 将question_model这个参数传入到'detail.html'中
    return render_template('detail.html', question=question_model)

@app.route('/add_content/', methods=['POST'])
@login_required
def content():
    content = request.form.get('content')
    question_id = request.form.get('question_id')

    answer = Answer(content=content)
    user_id = session['user_id']
    user = User.query.filter(User.id == user_id).first()
    answer.author = user
    question = Question.query.filter(Question.id == question_id).first()
    answer.question = question



    db.session.add(answer)
    db.session.commit()




    return redirect(url_for('detail', question_id=question_id))

@app.route('/search/')
def search():
    q = request.args.get('q')
    # 关键字可能在title也可能在content中
    questions = Question.query.filter(or_(Question.title.contains(q),
    Question.content.contains(q))).order_by('-create_time')
    return render_template('index.html', questions=questions)

if __name__ == '__main__':
    app.run()
