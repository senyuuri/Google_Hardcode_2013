from google.appengine.ext import db

'''
Subject List:
15 -- all
0 -- General Paper
1 -- Mathematics
2 -- Physics
3 -- Chemistry
4 -- Economy
5 -- Biology
6 -- Geography
7 -- Computing
8 -- ELL
9 -- CLL
10 -- CSC
11 -- GSC
12 -- Art
13 -- Music
*14 -- Third Language

'''

class User(db.Model):
	user = db.UserProperty()
	nickname = db.StringProperty()
	#auth: 0 - admin, 1 - teacher, 2 - student
	auth = db.IntegerProperty()
	reg_time = db.DateTimeProperty(auto_now_add = True)
	last_login = db.DateTimeProperty()
	forgetpw = db.StringProperty()
	post_num = db.IntegerProperty()
	comment_num = db.IntegerProperty()
	subcombi = db.ListProperty(str)
	#relevant_post = db.ReferenceProperty(Post,collection_name='postuser')


class Post(db.Model):
	pid = db.IntegerProperty()
	title = db.StringProperty(multiline = False)
	content = db.StringProperty(str)
	subject = db.IntegerProperty()

	post_time = db.DateTimeProperty(auto_now_add = True)
	last_modified = db.DateTimeProperty()
	comment_num = db.IntegerProperty()
	like = db.IntegerProperty()
	post_user = db.UserProperty(required = True)
	relevant_user = db.ReferenceProperty(User, collection_name='posts')

	answer = db.StringProperty(str)
	answer_user = db.UserProperty()
	#have answer = 1, not = 0
	status = db.IntegerProperty()


class Comment(db.Model):
	cid = db.IntegerProperty()
	content = db.StringProperty(multiline = True)
	like = db.IntegerProperty()
	post_user = db.UserProperty(required = True)
	post_time = db.DateTimeProperty(auto_now_add = True)
	relevant_post = db.ReferenceProperty(Post,collection_name="comments")
	relevant_user = db.ReferenceProperty(User,collection_name='comments')