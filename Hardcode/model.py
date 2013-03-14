from google.appengine.ext import db
import hashlib



secret="Metallica"



class User(db.Model):
    uid = db.IntegerProperty()
    name = db.StringProperty(required = True)
    pw = db.StringProperty(required = True)
    email = db.StringProperty(required = True)
    auth = db.IntegerProperty()
    #post_list = db.ListProperty((int,indexed=True,default=None))
    reg_time = db.DateTimeProperty(auto_now_add = True)
    question = db.StringProperty(required=True)
    answer=db.StringProperty(required=True)
    
    @classmethod
    def login(cls,name,pw):
        u=User.all().filter('name =',name).get()
        if u and u.pw==str(hashlib.sha256(secret+pw+secret).hexdigest()):
            return u

class Post(db.Model):
    pid = db.IntegerProperty()
    title = db.StringProperty(multiline = False)
    content = db.TextProperty()
    date = db.DateTimeProperty(auto_now_add = True)
    user = db.ReferenceProperty(User, collection_name='posts')
    price = db.IntegerProperty()
    like = db.IntegerProperty()
    expire = db.IntegerProperty()
    strcontent=db.StringProperty()  
class Log(db.Model):
    lid=db.IntegerProperty()
    log_time=db.DateTimeProperty(auto_now_add=True)
    log_type=db.StringProperty()

    from_user=db.ReferenceProperty(User,collection_name="logs")
    
    to_user=db.ReferenceProperty(User)

    relevant_post=db.ReferenceProperty(Post,collection_name="modifications")



def next_post_id():
    posts = db.GqlQuery('SELECT * FROM Post ORDER BY pid DESC')
    return 0 if posts.count() == 0 else posts[0].pid + 1
def next_log_id():
    logs=db.GqlQuery('SELECT * FROM Log ORDER BY lid DESC')
    return 0 if logs.count() == 0 else logs[0].lid+1
def next_user_id():
    users = db.GqlQuery('SELECT * FROM User ORDER BY uid DESC')
    return 0 if users.count() == 0 else users[0].uid+1
"""
def put_post(title, content):
    post = Post()
    post.pid = next_post_id()
    post.title = title
    post.content = content

    post.put()

def put_user(name,pw,email):
    user = User()
    user.uid=next_user_id()
    user.name=name
    user.pw=pw
    user.email=email
    user.auth=1
    user.put()
"""
@db.transactional
def update_post(key, title,content,price):
    obj = db.get(key)
    obj.title= title
    obj.content=content
    obj.price=price
    obj.put()

