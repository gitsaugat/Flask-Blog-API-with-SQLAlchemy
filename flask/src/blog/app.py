from flask import Flask 
from flask import render_template
from flask import url_for
from flask import request
from flask import redirect
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime 
app = Flask(__name__)
posts = [

       {
       'title':'Blog 1',
       'author':'Saugat',
       'date':'2019-12-23',
       'content':'Blog POst 1',

       },
       {
       'title':'Blog 1',
       'author':'Saugat',
       'date':'2019-12-23',
       'content':'Blog POst 1',

       }
]
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)
class Post(db.Model):
	id = db.Column(db.Integer , primary_key = True)
	author = db.Column(db.String(50) , nullable = False)
	title = db.Column(db.String(200) , nullable = False)
	content = db.Column(db.Text , nullable = False)
	date = db.Column(db.DateTime , default = datetime.utcnow )

	def __repr__(self):
		return 'Post - %r' %self.id 
		#post - id(default  primary key of post)


@app.route('/')
@app.route('/home')
def homepage():
	return render_template('home.html' , title = 'Home' , posts = Post.query.all())
@app.route('/addpost' , methods = ['GET' , 'POST'])
def add():
	if request.method == 'POST':
		title  = request.form['title']
		content = request.form['content']
		author = request.form['author']
		new  = Post(author = author , title = title , content = content)
		db.session.add(new)
		db.session.commit()
		return redirect('/')

	return render_template('add.html' , title  = ' +post ' )
@app.route('/this/edit/<int:id>' , methods = ['GET' , 'POST'])
def edit(id):
	post = Post.query.get_or_404(id)
	if request.method == 'POST':
		post.title = request.form['title']
		post.content = request.form['content']
		post.author = request.form['author']
		db.session.commit()
		return redirect('/')
	return render_template('edit.html' , title = 'Delete' , post = post)
@app.route('/this/delete/<int:id>' )
def delete(id):
	post = Post.query.get_or_404(id)
	db.session.delete(post)
	db.session.commit()
	return redirect('/')
@app.route('/this/post/<int:id>' )
def post(id):
	post = Post.query.get_or_404(id)
	
	return render_template('this.html' , title = 'POst' , post = post)
if __name__  == '__main__':

	app.run(debug = True)


