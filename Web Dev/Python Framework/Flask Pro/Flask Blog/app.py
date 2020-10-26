from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)   

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "Verysecret"

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    blogs = db.relationship('BlogPost', backref='user', lazy=True)

    def __repr__(self):
        return self.name


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    author = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(225), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime , nullable = False, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/', methods=['GET','POST'])
def index():
    blogs = BlogPost.query.all()
    return render_template('index.html', rec = False, blogs = blogs)


@app.route('/<int:id>')
def blogread(id):
    blog = BlogPost.query.get_or_404(id)
    return render_template('read.html', blog = blog)


@app.route('/profile')
@login_required
def profile():
    blogs = BlogPost.query.filter_by(user_id = current_user.id).all()
    return render_template('profile.html', user = current_user, blogs = blogs)


@app.route('/profile/blog', methods=['GET', 'POST'])
@login_required
def profileblog():
    if request.method == 'POST':
        new_blog = BlogPost(author = current_user.name, title = request.form.get('title'), desc = request.form.get('desc'), 
        content = request.form.get('content'), user_id = current_user.id)
        db.session.add(new_blog)
        db.session.commit()
        return redirect( url_for('profile'))
    return render_template('createblog.html', user = current_user)


@app.route('/profile/blog/delete/<int:id>')
@login_required
def delete_blog(id):
    blog = BlogPost.query.get_or_404(id)
    db.session.delete(blog)
    db.session.commit()
    return redirect(url_for('profile'))


@app.route('/profile/blog/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edid_blog(id):
    blog = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        blog.title = request.form.get('title')
        blog.content = request.form.get('content')
        blog.desc = request.form.get('desc')
        db.session.commit()
        return redirect(url_for('profile'))
    return render_template('edit.html', blog = blog, user = current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        name = request.form.get('name')
        password = request.form.get('password')
        all_users = User.query.filter_by(name = name).all()
        for i in all_users:
            if i.password == password and i.name == name:
                user = User.query.get(i.id)
                load_user(user.id)
                login_user(user)
                return redirect(url_for('profile'))
    return render_template('login.html', signup = False)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        if request.form.get('pass1') == request.form.get('pass2'):
            user = User(name = request.form.get('name'), email = request.form.get('email'), password = request.form.get('password'))
            db.session.add(user)
            db.session.commit()
            load_user(user.id)
            login_user(user)
            return redirect( url_for('profile'))
    return render_template('login.html', signup = True)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect( url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)