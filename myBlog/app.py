from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os 
from datetime import datetime

app = Flask(__name__)

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "blog.db"))

app.config['SQLALCHEMY_DATABASE_URI'] = database_file

db = SQLAlchemy(app)

class BlogPost(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(50))
	subtitle = db.Column(db.String(50))
	author = db.Column(db.String(20))
	image = db.Column(db.String(100))
	quote = db.Column(db.String(50))
	date_posted = db.Column(db.DateTime)
	content = db.Column(db.Text)

@app.route('/')
def index():
	posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).all()
	return render_template('index.html', posts = posts)

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/contact')
def contact():
	return render_template('contact.html')

@app.route('/portfolio')
def portfolio():
	return render_template('portfolio.html')

@app.route('/add')
def add():
	return render_template('addPost.html')

@app.route('/post/<int:post_id>')
def post(post_id):
	post = BlogPost.query.filter_by(id = post_id).one()
	return render_template('post.html', post = post)

@app.route('/addPost', methods=['POST'])
def addPost():
	title = request.form['title']
	subtitle = request.form['subtitle']
	author = request.form['author']
	content = request.form['content']
	image = request.form['image']
	quote = request.form['quote']
	post = BlogPost(title = title, date_posted = datetime.now(), image = image, quote = quote, subtitle = subtitle, author = author, content = content)

	db.session.add(post)
	db.session.commit()

	return redirect(url_for('index'))

if __name__ == "__main__":
	app.run(debug=True) 