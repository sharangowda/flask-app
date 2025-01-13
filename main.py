from flask import Flask, redirect, render_template, request, session
from wtforms import Form, StringField, PasswordField, validators
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, Null, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import uuid


class User:
    def __init__(self):
        self.username = ""
        self.password = ""


class Base:
    pass


app = Flask(__name__)
db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///posts_data.db"
db.init_app(app=app)
app.secret_key = "123456"


# Forms


class SigninForm(Form):
    username = StringField("username", render_kw={"placeholder": "test"})
    password = PasswordField("password", render_kw={"placeholder": "password"})


class PostForm(Form):
    title = StringField('title',  [validators.InputRequired(), validators.Length(max=50)], render_kw={
                        "placeholder": "Title of the post"})
    body = StringField('body', [validators.InputRequired(), validators.Length(
        max=200)], render_kw={"placeholder": "Body of the post"})


class Database(db.Model):
    id: Mapped[str] = mapped_column(String, primary_key=True)
    post_title: Mapped[str] = mapped_column(String, unique=False)
    body: Mapped[str] = mapped_column(String(), nullable=False)
    comments: Mapped[str] = mapped_column(String(), nullable=True)
    likes: Mapped[int] = mapped_column(Integer, nullable=False)


class Posts(Database):
    def __init__(self):
        self.id = ""
        self.post_title = ""
        self.body = ""
        self.comments = ""
        self.likes = 0

    def increaseId(self):
        self.id += 1


with app.app_context():
    db.create_all()


@app.route("/", methods=['GET', 'POST'])
def Hello():
    form = SigninForm()
    if request.method == "POST":
        user = User()
        user.username = request.form['username']
        user.password = request.form['password']
        if user.username == "admin" and user.password == "123":
            return redirect('/home')
        else:
            return redirect('/denied')
    return render_template('index.html', form=form)


@app.route("/home")
def home():
    return render_template('home.html')


@app.route('/denied')
def denied():
    return render_template('denied.html')


@app.route('/create-post', methods=['GET', 'POST'])
def createPost():
    form = PostForm()
    if request.method == "POST":
        post = Posts()
        post.id = str(uuid.uuid4())
        post.post_title = request.form['title']
        post.body = request.form['body']
        post.likes = 0
        db.session.add(post)
        db.session.commit()
    return render_template('create-post.html', form=form)


@app.route('/view-post')
def viewPost():
    posts = db.session.execute(select(Posts).order_by(Posts.id)).scalars()
    new_posts = posts.all()
    return render_template('view-post.html', posts=new_posts)


@app.route('/<postId>')
def postPage(postId):
    postBody = db.session.execute(select(Posts).filter_by(id=postId)).scalar()
    title = postBody.post_title
    body = postBody.body
    comment = postBody.comments
    likes = postBody.likes
    return render_template('post-page.html', id=postId, title=title, body=body, comment=comment, likes=likes)


if __name__ == "__main__":
    app.run(debug=True)
