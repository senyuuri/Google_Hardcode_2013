import os
import re
import random
import hashlib
import hmac
from string import letters
from datetime import datetime
import time
from google.appengine.api import mail
#from time import gmtime, strftime

import webapp2
import jinja2

from google.appengine.ext import db

import model

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

secret="Metallica"

def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class BaseHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
#        params['user'] = self.user
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'username=; Path=/')
        self.response.headers.add_header('Set-Cookie','username=; Path=/')

#    def initialize(self, *a, **kw):
#        webapp2.RequestHandler.initialize(self, *a, **kw)
#        uid = self.read_secure_cookie('user_id')
#        self.user = uid and model.User.by_id(int(uid))

    def login(self, user):
        self.set_secure_cookie(user)
        self.set_password_cookie(user)
        


    def set_secure_cookie(self, name):
        #cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            'username=%s; Path=/' % str(name))

    def set_password_cookie(self,name):
        u=db.GqlQuery("SELECT * FROM User WHERE name = :1",name)
        user=u[0]
        self.response.headers.add_header(
            'Set-Cookie',
            'auth=%s; Path=/' % str(hashlib.sha256(name+secret+user.pw).hexdigest()))

    def read_secure_cookie(self, name):
        cookie_val = ""
        if not self.request.cookies.get(name)==None:
            cookie_val = str(self.request.cookies.get(name))
        return cookie_val

    def validate(self,name):
        user=db.GqlQuery("SELECT * FROM User WHERE name =:1",name).get()
        if not user:
            return False
        elif self.read_secure_cookie("auth")!=str(hashlib.sha256(name+secret+user.pw).hexdigest()):
            return False
        else:
            return True
    def email(self, sender,recipient,subject,content):
        mail.send_mail(sender=sender,
                              to=recipient,
                              subject=subject,
                              body=content)

       

    
class MainPage(BaseHandler):
  def get(self):
        
        posts = db.GqlQuery("SELECT * FROM Post order by date desc limit 10") 
        posts = model.Post.all().filter('expire >',0)
        Username = self.read_secure_cookie('username')
        u=db.GqlQuery("SELECT * FROM User WHERE name = :1",Username).get()
        self.render('index.html',posts=posts, user=Username, PageTitle="")
     


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

PRICE_RE = re.compile(r"^[0-9]{1,7}$")
def valid_price(price):
    return price and PRICE_RE.match(price)

class Signup(BaseHandler):

    def get(self):
        self.render('signup-form.html',PageTitle="Sign Up")

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        question=self.request.get("question")
        answer=self.request.get('answer')


        params = dict(username = username,
                      email = email, PageTitle="Sign Up")

        u=model.User.all().filter('name =',username).get()
        if u:
            params['error_username'] = "Username already exists."
            have_error = True            

        if not valid_username(username):
            params['error_username'] = "Username not valid.(only alphabet, numbers and _ - allowed)"
            have_error = True

        if not valid_password(password):
            params['error_password'] = "Password not vaild.(3 < length < 20)"
            have_error = True
        elif password != verify:
            params['error_verify'] = "Password not match."
            have_error = True

        if not valid_email(email):
            params['error_email'] = "Email not vaild."
            have_error = True

        if not question:
            params['error_question']="Please enter your question"
            have_error=True

        if not answer:
            params['error_answer']='Please enter answer to your question'
            have_error=True

        if have_error:
            self.render('signup-form.html', **params)
        else:
            u = model.User(name = username, pw = str(hashlib.sha256(secret+password+secret).hexdigest()),auth=1, email = email,question=question,answer=str(hashlib.sha256(secret+answer+secret).hexdigest()))
            u.uid=model.next_user_id()
            u.put()
            log=model.Log(from_user=u,log_type="Signup",lid=model.next_log_id())
            log.put()
            log=model.Log(from_user=u,log_type="Login",lid=model.next_log_id())
            log.put()
            self.redirect('/?username=' + username)
            self.set_secure_cookie(str(username))
            self.set_password_cookie(str(username))
            #self.redirect('/welcome?username=' + username)
            

class Welcome(BaseHandler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.render('welcome.html', username = username, PageTitle="Welcome")
        else:
            self.redirect('/signup')


class Login(BaseHandler):
    def get(self):
        self.render('login-form.html',PageTitle="Login",)

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = model.User.login(username, password)
        if u:
            self.login(u.name)
            log=model.Log(from_user=u,log_type="Login",lid=model.next_log_id())
            log.put()
            self.redirect('/?username=' + username)
        else:
            msg = 'Invalid login'
            self.render('login-form.html', error = msg,PageTitle="Login")

class Logout(BaseHandler):
    def get(self):
        Username=self.read_secure_cookie('username')
        u=db.GqlQuery('SELECT * FROM User WHERE name=:1',Username)
        user = u[0]
        log=model.Log(from_user=user,log_type="Logout",lid=model.next_log_id())
        log.put()
        self.logout()
        self.redirect('/')

class Account(BaseHandler):
    def get(self):
        Username = self.read_secure_cookie('username')
        if not self.validate(Username):
            self.logout()
            self.redirect('/')
        
        if Username:
            u=db.GqlQuery('SELECT * FROM User WHERE name=:1',Username)
            user = u[0]
            posts = user.posts
            self.render("account.html", USER = user, posts=posts, user=Username)
        else:
            self.redirect('/login')

    def post(self):
        Username = self.read_secure_cookie('username')
        if not self.validate(Username):
            self.logout()
            self.redirect('/')
        Pid = int(self.request.get('pid'))
        p = db.GqlQuery('SELECT * FROM Post WHERE pid=:1', Pid).get()
        db.delete(p)
        
        self.redirect('/account')


class Profile(BaseHandler):
    def get(self, Username):
        u=db.GqlQuery('SELECT * FROM User WHERE name=:1',Username).get()
        if not u:
            self.redirect('/')
        else:
            u=db.GqlQuery('SELECT * FROM User WHERE name=:1',Username)
            user = u[0]
            posts = user.posts
            self.render("profile.html", USER = user, posts=posts, user=Username)

class Delete(BaseHandler):
    def get(self):
        Username = self.read_secure_cookie('username')
        if not self.validate(Username):
            self.logout()
            self.redirect('/')
        
        option = self.request.get('option')
        if Username:
            if option == 'Delete Your Account':
                u=db.GqlQuery('SELECT * FROM User WHERE name=:1',Username)
                user = u[0]
                log=model.Log(from_user=user,log_type="Delete_All",lid=model.next_log_id())
                log.put()
                posts = user.posts
                db.delete(posts)
                us=db.GqlQuery('SELECT * FROM User WHERE name=:1',Username).get()
                db.delete(us)
                self.logout()


                self.redirect('/')
            if option == 'Delete All Your User Data':
                u=db.GqlQuery('SELECT * FROM User WHERE name=:1',Username)
                user = u[0]
                posts = user.posts
                db.delete(posts)
                log=model.Log(from_user=user,log_type="Delete_All_Data",lid=model.next_log_id())
                log.put()
                self.redirect('/account')
        else:
            self.redirect('/')
            

class AddPost(BaseHandler):
    def get(self):
        
        Username = self.read_secure_cookie('username')
        if not self.validate(Username):
            self.logout()
            self.redirect('/')
        u=db.GqlQuery("SELECT * FROM User WHERE name = :1",Username).get()
        if u:
            self.render("add_post.html",PageTitle="Add Items", user=u.name)
        else:
            self.redirect('/login')

    def post(self):
        Username = self.read_secure_cookie('username')
        if not self.validate(Username):
            self.logout()
            self.redirect('/')
        have_error=False
        error=""
        title=self.request.get('title')
        content=self.request.get('content')
        price=self.request.get('price')
        expire=30
        '''
        if expire.month==12:
            expire=expire.replace(year=expire.year+1,month=1)
        else:
            expire=expire.replace(month=expire.month+1)
        '''
        Username = self.read_secure_cookie('username')
        

        if not valid_price(price):
            error="That's not a vaild price"
            self.render("add_post.html",title=title,content=content,error=error,PageTitle="Add Items")
        
        elif title and content:
            u=db.GqlQuery('SELECT * FROM User WHERE name=:1',Username)
            user = u[0]
            p=model.Post(title=title,content=content,user=user,price=int(price),like=0,expire=expire,strcontent=str(title)+str(content))
            p.pid=model.next_post_id()
            p.put()
            log=model.Log(from_user=user,log_type="Add_Item",relevant_post=p,lid=model.next_log_id())
            log.put()
            self.redirect('/')
        '''
        else:
            error="title and content please"
            self.render("add_post.html",title=title,content=content,error=error,PageTitle="Add Items")
        '''

class ViewSinglePost(BaseHandler):
    def get(self,pid):
        posts=db.GqlQuery('SELECT * FROM Post WHERE pid = :1', int(pid))
        post=posts[0]
        if not post:
            self.error(404)
            return

        Username = self.read_secure_cookie('username')
        self.render("single_post.html",post=post,PageTitle="View Post", user=Username)
    def post(self,pid):
        posts=db.GqlQuery('SELECT * FROM Post WHERE pid = :1', int(pid))
        post=posts[0]
        if not post:
            self.error(404)
            return        
        post.like+=int(self.request.get("like"))
        Username = self.read_secure_cookie('username')
        self.render("single_post.html",likenum=post.like,post=post,PageTitle="View Post", user=Username)
class EditPost(BaseHandler):
    def get(self,pid):
        
        Username = self.read_secure_cookie("username")
        if not self.validate(Username):
            self.logout()
            self.redirect('/')
        posts=db.GqlQuery('SELECT * FROM Post WHERE pid = :1', int(pid))
        post=posts[0]
        if not post:
            self.error(404)
            return
        elif post.user.name == Username or self.check_admin(Username):  
            self.render("edit_post.html",PageTitle="Edit a Post", user=Username,title=post.title,content=post.content,price=str(post.price))
        else:
            self.redirect('/')

    def post(self,pid):
        
        Username = self.read_secure_cookie("username")
        if not self.validate(Username):
            self.logout()
            self.redirect('/')
        u=db.GqlQuery('SELECT * FROM User WHERE name=:1',Username)
        user = u[0]
        title=self.request.get("title")
        content=self.request.get('content')
        price=self.request.get('price')
        #pid=self.request.get("post_id")
        if title and content:
            p=db.GqlQuery("SELECT * FROM Post WHERE pid =:1",int(pid))
            acc=p.get()
            model.update_post(acc.key(),title,content,int(price))
            log=model.Log(from_user=user,log_type="Edit_Item",relevant_post=acc,lid=model.next_log_id())
            log.put()
            self.redirect("/")
        else:
            error="title and content please"
            self.render("edit_post.html",title=title,user=Username, content=content,price=price,error=error,PageTitle="Edit a Post")


class ResetPassword(BaseHandler):
    def get(self):
        self.render('reset_password_1.html')
    def post(self):
        have_error = False
        username = self.request.get('username')
        email = self.request.get('email')

        params = dict(username = username,
                      email = email)
        users=db.GqlQuery("SELECT * FROM User WHERE name = :1",username)
        user=users.get()

        if not user:
            params['error_username'] = "User does not exist."
            have_error = True

        if (not have_error) and user.email!=email:
            params['error_email'] = "username does not match email."
            have_error = True

        if (not have_error) and not valid_username(username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if (not have_error) and not valid_email(email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('reset_password_1.html', **params)
        else:
            self.set_secure_cookie(username)
            self.redirect('/reset_verify')

class Verify(BaseHandler):
    def get(self):
        username=self.read_secure_cookie('username')
        users=db.GqlQuery("SELECT * FROM User WHERE name = :1",username)
        user=users.get()
        if not user:
            self.response.out.write("User does NOT exist")
        else:
            self.render("reset_password_2.html",username=username,question=user.question)

    def post(self):
        username=self.read_secure_cookie('username')
        answer=self.request.get("answer")
        user=db.GqlQuery("SELECT * FROM User WHERE name = :1",username).get()
        if not answer:
            error_answer="Please enter your answer"
            self.render("reset_password_2.html",username=username,question=user.question,error_answer=error_answer)
        if str(hashlib.sha256(secret+answer+secret).hexdigest())!=user.answer:
            error="Answer NOT correct"
            self.render("reset_password_2.html",username=username,question=user.question,error_answer=error)
        else:
            password=self.request.get("password")
            verify=self.request.get('verify')
            have_error=False

            params = dict(username = username,question=user.question,answer=answer)

            if not valid_password(password):
                params['error_password'] = "That wasn't a valid password."
                have_error = True
            elif password != verify:
                params['error_verify'] = "Your passwords didn't match."
                have_error = True

            if have_error:
                self.render("reset_password_2.html",**params)
            else:
                user.pw=str(hashlib.sha256(secret+password+secret).hexdigest())
                user.put()
                log=model.Log(from_user=user,log_type="Reset_Password",lid=model.next_log_id())
                log.put()
                sender_email="Metallica_Project reset_password@ps-application.appspotmail.com"
                mailbody=("""
Dear """+user.name+""": 

You have changed your password. Please reset your password if this is not your own action.

Please let us know if you have any queries.

Regards,
The Metallica Team
""")
                mail.send_mail(sender=sender_email,
                              to=user.email,
                              subject="Your password has been reset!",
                              body=mailbody)
                self.redirect('/')


#Daily Expiration Check
class Expire(BaseHandler):
    def get(self):
        self.response.out.write("Exp!")
        posts = db.GqlQuery("SELECT * FROM Post order by date")
        for i in posts:
            exp_time=i.expire
            if (exp_time-1)>=0:
                exp_time -= 1
                obj = db.get(i.key())
                obj.expire=exp_time
                obj.put()
                

class Search(BaseHandler):
    #def get(self):
    #    self.render("search.html",current1="Search by Title and Content", current2="Price",current3="Ascending",PageTitle="Search by Title and Content")
    def get(self):
        
        Username = self.read_secure_cookie("username")
        if not self.validate(Username):
            self.logout()
            self.redirect('/')
        searchtype=self.request.get('search_type')
        content=self.request.get('searchcontent')
        criteria1=self.request.get('criteria1')
        criteria2=self.request.get('criteria2')
        if not criteria1:
            criteria1="price"
        if not criteria2:
            criteria2="ASC"
        gqlcomm="SELECT * FROM Post ORDER BY "+criteria1+" "+criteria2
        posts = db.GqlQuery(gqlcomm)
        resultnum=0
        results=[]
        resultsid=[]
        resultsprice=[]
        resultsuser=[]
        resultsdate=[]
        seq=[]
        if searchtype=="content":
            searchlist=content.split(" ")
            for post in posts:
                fit=True
                for searchitem in searchlist:
                    if not searchitem in post.strcontent:
                        fit=False
                        break
                if fit:
                    resultnum+=1
                    seq.append(resultnum-1)
                    results.append(post.title)
                    resultsid.append(post.pid)
                    resultsprice.append(post.price)
                    resultsuser.append(post.user.name)
                    resultsdate.append(post.date)
                    
        else:
            if content!='':
                searchlist=int(content)
            else:
                searchlist=0
            for post in posts:
                if (searchlist*90<=int(post.price)*100<searchlist*110):
                    resultnum+=1
                    seq.append(resultnum-1)
                    results.append(post.title)
                    resultsid.append(post.pid) 
                    resultsprice.append(post.price)
                    resultsuser.append(post.user.name)
                    resultsdate.append(post.date)
        params=dict(PageTitle="Search Result",user=Username,searchcontent=content,seq=seq,resultnum=str(resultnum)+" result(s) found",resultsuser=resultsuser,resultsdate=resultsdate,resultsprice=resultsprice,resultsid=resultsid,results=results)
        cri1=""
        cri2=""
        cri3=""
        if searchtype=="content":
            cri1="Search by Title and Content"
            params["current1"]=cri1
            params["selectedcontent"]="selected"
        if searchtype=="price":
            cri1="Search by Price"
            params["current1"]=cri1
            params["selectedprice"]="selected"
        if criteria1=="price": 
            cri2="Price"
            params["current2"]=cri2
            params["selected1price"]="selected"
        if criteria1=="date": 
            cri2="Date"
            params["current2"]=cri2
            params["selected1date"]="selected"
        if criteria1=="user": 
            cri2="User"
            params["current2"]=cri2
            params["selected1user"]="selected"
        if criteria1=="like": 
            cri2="Like"
            params["current2"]=cri2
            params["selected1like"]="selected"
        if criteria2=="ASC": 
            cri3="Ascending"
            params["current3"]=cri3
            params["selected2asc"]="selected"
        if criteria2=="DESC": 
            cri3="Descending"
            params["current3"]=cri3
            params["selected2desc"]="selected"
        self.render("search.html/",**params)#PageTitle="Search Result",user=Username,current1=cri1,current2=cri2,current3=cri3,searchcontent=content,seq=seq,resultnum=str(resultnum)+" result(s) found",resultsuser=resultsuser,resultsdate=resultsdate,resultsprice=resultsprice,resultsid=resultsid,results=results)
    

class Editlist(BaseHandler):
    def get(self):
        
        Username = self.read_secure_cookie("username")
        if not self.validate(Username):
            self.logout()
            self.redirect('/')
        if Username:
            u=db.GqlQuery('SELECT * FROM User WHERE name=:1',Username)
            user = u[0]
            posts = user.posts
            self.render('edit_all.html',user=Username,PageTitle="Edit Items",posts=posts)
        else:
            self.redirect('/login')
    '''
    def post(self):
        Pid = int(self.request.get('pid'))
        p = db.GqlQuery('SELECT * FROM Post WHERE pid=:1', Pid).get()
        db.delete(p)    
        self.redirect('/editlist')
    '''
    
class Expired(BaseHandler):
    def get(self):
        
        Username = self.read_secure_cookie("username")
        if not self.validate(Username):
            self.logout()
            self.redirect('/')
        if Username:
            u=db.GqlQuery('SELECT * FROM User WHERE name=:1',Username)
            user = u[0]
            posts = user.posts.filter('expire <=', 0)
            self.render('edit_all.html',user=Username,PageTitle="Edit Items",posts=posts)
        else:
            self.redirect('/login')

class Available(BaseHandler):
    def get(self):
        Username = self.read_secure_cookie("username")
        if not self.validate(Username):
            self.logout()
            self.redirect('/')
        if Username:
            u=db.GqlQuery('SELECT * FROM User WHERE name=:1',Username)
            user = u[0]
            posts = user.posts.filter('expire >', 0)
            self.render('edit_all.html',user=Username,PageTitle="Edit Items",posts=posts)
        else:
            self.redirect('/login')

class ViewLog(BaseHandler):
    def get(self):
        
        Username = self.read_secure_cookie("username")
        if not self.validate(Username):
            self.logout()
            self.redirect('/')

        u=db.GqlQuery('SELECT * FROM User WHERE name=:1',Username)
        user = u[0]
        if user.auth==0:
            logs=db.GqlQuery('SELECT * From Log ORDER BY log_time DESC')
            self.render("logs.html",logs=logs,user=Username)
        else:
            self.redirect('/')

class Delone(BaseHandler):
    def get(self,pid):
        
        p = db.GqlQuery('SELECT * FROM Post WHERE pid=:1', int(pid)).get()
        if p:
            db.delete(p) 
        self.redirect('/editlist')

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/signup', Signup),
                               ('/welcome', Welcome),
                               ('/login', Login),
                               ('/add_post',AddPost),
                               ('/view/(.*)',ViewSinglePost),
                               ('/logout',Logout),
                               ('/account', Account),
                               ('/editlist', Editlist),
                               ('/available', Available),
                               ('/expired', Expired),
                               ('/delete', Delete),
                               ('/edit/(.*)',EditPost),
                               ('/admin/expire', Expire),
                               ('/profile/(.*)', Profile),
                               ('/reset',ResetPassword),
                               ('/reset_verify',Verify),
                               ('/search',Search),
                               ('/delone/(.*)',Delone),
                               #('/searchcontent',SearchContent),
                               #('/searchprice',SearchPrice),
                               ('/logs',ViewLog)
                               ],
                              debug=True)
