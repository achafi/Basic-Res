import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user 
import requests
import ref
import json 


app = Flask(__name__)


with open("info.json", "r") as c:
    parameters = json.load(c)["parameters"]

#app.config['YOUTUBE_API_KEY'] = parameters['key']
app.config['SQLALCHEMY_DATABASE_URI'] = parameters["database"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = parameters["track_modifications"]
app.config['SECRET_KEY'] = parameters["secret_key"]

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    comtext = db.Column(db.Text(), nullable=False)

    def __str__(self):
        return self.name


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    info = db.relationship('Userinfo', backref='user', lazy=True)

    def __repr__(self):
        return self.name


class Userinfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recent_watch_1 = db.Column(db.String(50), nullable=False)
    recent_watch_2 = db.Column(db.String(50), nullable=False)
    recent_watch_3 = db.Column(db.String(50), nullable=False)
    ml_recome_1 = db.Column(db.String(100), nullable=False)
    ml_recome_2 = db.Column(db.String(100), nullable=False)
    ml_recome_3 = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/', methods=['POST', 'GET'])
def index():
    videos = ref.youvideo()
    return render_template('index.html', user = False, namehead = "Get Recomendations", videos = videos)


@app.route('/comment', methods=['POST', 'GET'])
def comment():
    if request.method == 'POST':
        comment = Comments(name = request.form.get('namecom'), email = request.form.get('emailcom'), comtext = request.form.get('comtext'))
        db.session.add(comment)
        db.session.commit()
        videos = ref.youvideo()
        if current_user.is_authenticated:
            return redirect( url_for('user'))
        return render_template('index.html', user = False, namehead = "Get Recomendations", msg = "Comment saved", videos = videos)
    return '''
    <a href="/" style="color:white;">Home page</a>
    '''


@app.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        userInput = [
            {'title':request.form.get('title1'), 'rating':float(request.form.get('rating1'))},
            {'title':request.form.get('title2'), 'rating':float(request.form.get('rating2'))},
            {'title':request.form.get('title3'), 'rating':float(request.form.get('rating3'))},
            {'title':request.form.get('title4'), 'rating':float(request.form.get('rating4'))},
            {'title':request.form.get('title5'), 'rating':float(request.form.get('rating5'))},
            {'title':request.form.get('title6'), 'rating':float(request.form.get('rating6'))},
            {'title':request.form.get('title7'), 'rating':float(request.form.get('rating7'))},
            {'title':request.form.get('title8'), 'rating':float(request.form.get('rating8'))},
            {'title':request.form.get('title9'), 'rating':float(request.form.get('rating9'))},
            {'title':request.form.get('title10'), 'rating':float(request.form.get('rating10'))},
        ]
        predict = ref.predict(userInput, request.form.get('o'))
        if current_user.is_authenticated:
            info = Userinfo(recent_watch_1 = request.form.get('title1'), recent_watch_2 = request.form.get('title2'), recent_watch_3 = request.form.get('title3'), ml_recome_1 = predict[0], ml_recome_2 = predict[1], ml_recome_3 = predict[2], user_id=current_user.id)
            db.session.add(info)
            db.session.commit()
            videos = ref.youvideoauth(predict)
            return render_template('index.html', videos = videos, predict = predict, namehead = "Recomendations", msg = "Enjoy", rec = True, user = current_user)
        videos = ref.youvideo()
        return render_template('index.html', predict = predict, rec = True, msg = "Here are some movies you might like", user = False, namehead = "Recomendations", videos = videos)
    return '''
    <a href="/" style="color:white;">Home page</a>
    '''


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    videos = ref.youvideo()
    if request.method == 'POST':
        if request.form.get('pass1') == request.form.get('pass2'):
            user = User(name = request.form.get('name'), email = request.form.get('email'), password = request.form.get('pass1'))
            db.session.add(user)
            db.session.commit()
            load_user(user.id)
            login_user(user)
            return redirect( url_for('user'))
        
        return render_template("index.html", namehead = "Get Recomendations", msg = "Password Error", user = False, videos = videos)
    return '''
    <a href="/" style="color:white;">Home page</a>
    '''


@app.route('/login', methods=['POST', 'GET'])
def login():
    videos = ref.youvideo()
    if request.method == "POST":
        name = request.form.get('name')
        password = request.form.get('password')
        all_users = User.query.filter_by(name = name).all()
        for i in all_users:
            if i.password == password and i.name == name:
                user = User.query.get(i.id)
                load_user(user.id)
                login_user(user)
                return redirect(url_for('user'))
            else :
                return render_template("index.html", namehead = "Get Recomendations", user = False, msg="Invalid user", videos = videos)
    return render_template("index.html", namehead = "Get Recomendations", user = False, msg="Create account to enjoy", videos = videos)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect( url_for('index'))


@app.route('/user', methods=['POST', 'GET'])
@login_required
def user():
    info = Userinfo.query.filter_by(user_id = current_user.id).first()   
    if info :
        a = [info.ml_recome_1, info.ml_recome_2, info.ml_recome_3]
        videos = ref.youvideoauth(a)
    else :
        videos = ref.youvideo()
    return render_template('index.html', namehead = "Get Recomendations", msg = "login success", user = current_user, videos = videos)


@app.route('/admin', methods=['POST', 'GET'])
def admin():
    if request.method == 'POST':
        if request.form.get('name') == 'admin' and request.form.get('password') == 'password' and request.form.get('email') == 'adminemail':
            all_users = User.query.all()
            all_comments = Comments.query.all()
            return render_template('admin.html', all_users=all_users, all_comments=all_comments, ua = True)
    return render_template('admin.html', ua = False)


if __name__ == "__main__":
    app.run(threaded=True)
