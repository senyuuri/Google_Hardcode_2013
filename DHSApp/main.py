import os
import re
import random
import hashlib
import hmac
from string import letters
from datetime import datetime
import time
from google.appengine.api import mail
from google.appengine.api import users
from google.appengine.ext import db

import webapp2
import jinja2



import model

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                                             autoescape = True)


def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

def next_post_id():
    posts = db.GqlQuery('SELECT * FROM Post ORDER BY pid DESC')
    return 0 if posts.count() == 0 else posts[0].pid + 1

def next_comment_id():
    posts = db.GqlQuery('SELECT * FROM Comment ORDER BY cid DESC')
    return 0 if posts.count() == 0 else posts[0].cid + 1

class BaseHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Login(BaseHandler):
    def get(self):
        user = users.get_current_user()
        params = {
                  'login': users.create_login_url("/"),
        }
        if user:
            self.redirect('/main')
        else:
            #self.response.out.write("login success")
            self.render('index.html',**params)



class MainPage(BaseHandler):
    def get(self):
        #self.response.out.write("test")
        user = users.get_current_user()
        u=db.GqlQuery('SELECT * FROM User WHERE user = :1', user).get()
        if not user:
            self.redirect('/')
        
        else:
            #First login initialisation
            if not u:
              newu=model.User(user=user,nickname=user.nickname(),auth=2,post_num=0,comment_num=0)
              u = newu
            u.last_login = datetime.now()
            u.put()
            
            sublist = ['General Paper','Mathematics','Physics','Chemistry','Economy','Biology','Geography','Computing','ELL','CLL','CSC','GSC','Art','Music','Third Language','All']
            temp_html=''
            subnum = u.subcombi
            subject = []
            for s in subnum:
              subject.append(sublist[int(s)])
              temp_html += ('<li><a href="/main/subject/%s">%s</a></li>'%(int(s),sublist[int(s)]))

            params = {
                'logout':users.create_logout_url("/"),
                'nickname':u.nickname,
                'temp_html':temp_html,
            }
            self.render('main.html',**params)

class Subject(BaseHandler):
    def get(self,pid):
        #self.response.out.write("test"+pid)
        user = users.get_current_user()
        u=db.GqlQuery('SELECT * FROM User WHERE user = :1', user).get()
        sublist = ['General Paper','Mathematics','Physics','Chemistry','Economy','Biology','Geography','Computing','ELL','CLL','CSC','GSC','Art','Music','Third Language','All']
        posts = db.GqlQuery("SELECT * FROM Post WHERE subject=:1 ORDER BY post_time desc limit 10",int(pid))
        
        
        params = {
                  'subject':sublist[int(pid)],
                  'posts':posts,
                  'logout':users.create_logout_url("/"),
                  'nickname':u.nickname,

        }

        
        #self.response.out.write(posts[0].title)
        self.render("subject.html",**params)

class AddPost(BaseHandler):
    def get(self):
        user = users.get_current_user()
        u=db.GqlQuery('SELECT * FROM User WHERE user = :1', user).get()
        params = {
                  'logout':users.create_logout_url("/"),
                  'nickname':u.nickname,

        }
        self.render("add_post.html",**params)
        
        #self.response.out.write("login success")

    def post(self):
        user = users.get_current_user()
        u=db.GqlQuery('SELECT * FROM User WHERE user = :1', user).get()
        title = self.request.get('title')
        subject = int(self.request.get('subject'))
        content = self.request.get('content')
        p = model.Post(relevant_user=u,title=title,subject=subject,content=content,post_user=user,status=0,comment_num=0,like=0)
        p.pid = next_post_id()
        p.put() 
        u.post_num=u.post_num+1
        u.put()
        #self.response.out.write(subject)
        self.redirect('/main')

class SinglePost(BaseHandler):
    def get(self,pid):
        posts=db.GqlQuery('SELECT * FROM Post WHERE pid = :1', int(pid))
        user = users.get_current_user()
        u=db.GqlQuery('SELECT * FROM User WHERE user = :1', user).get()
        p = posts.get()
        sublist = ['General Paper','Mathematics','Physics','Chemistry','Economy','Biology','Geography','Computing','ELL','CLL','CSC','GSC','Art','Music','Third Language','All']
        comments = p.comments
        params = {
                  'logout':users.create_logout_url("/"),
                  'nickname':u.nickname,
                  'post':p,
                  'subject':sublist[int(pid)],
                  'comments':comments,
        }
        if not posts:
          self.error(404)
          return
        #self.response.out.write(p.title)
        self.render('single_post.html',**params)

    def post(self,pid):
        user = users.get_current_user()
        postid = int(self.request.get('postid'))
        u=db.GqlQuery('SELECT * FROM User WHERE user = :1', user).get()
        p=db.GqlQuery('SELECT * FROM Post WHERE pid = :1', postid).get()
        comment = self.request.get('comment')
        c = model.Comment(post_user=user,content=comment,relevant_post=p,relevant_user=u)
        c.cid = next_comment_id()
        p.comment_num = p.comment_num + 1
        u.comment_num = u.comment_num + 1
        u.put()
        p.put()
        c.put()
        redir_url='/main/post/'+str(postid)
        self.redirect(redir_url)

class Profile(BaseHandler):
    def get(self,username):
        user = users.get_current_user()
        current_u=db.GqlQuery('SELECT * FROM User WHERE user = :1', user).get()
        u=db.GqlQuery('SELECT * FROM User WHERE nickname = :1', username).get()
        #self.response.out.write(username)
        posts = u.posts
        comments = u.comments

        sublist = ['General Paper','Mathematics','Physics','Chemistry','Economy','Biology','Geography','Computing','ELL','CLL','CSC','GSC','Art','Music','Third Language','All']
        subnum = u.subcombi
        subject = []
        for s in subnum:
          subject.append(sublist[int(s)])
          
        #self.response.out.write(subject) 
        if not u:
          self.error(404)
          return
        
        if u.auth == 0:
          group = 'admin'
        elif u.auth == 1:
          group = 'teacher'
        else:
          group = 'student'
        params = {
                  'logout':users.create_logout_url("/"),
                  'nickname':current_u.nickname,
                  'user':u,
                  'group':group,
                  'posts':posts,
                  'comments':comments,
                  'subject':subject,
        }
        self.render('profile.html', **params)        


class Account(BaseHandler):
    def get(self):
      #self.response.out.write('test')
      user = users.get_current_user()
      current_u=db.GqlQuery('SELECT * FROM User WHERE user = :1', user).get()
      sublist = ['General Paper','Mathematics','Physics','Chemistry','Economy','Biology','Geography','Computing','ELL','CLL','CSC','GSC','Art','Music','Third Language','All']
      subnum = current_u.subcombi
      subject = []
      for s in subnum:
        
        subject.append(sublist[int(s)])
        #self.response.out.write(subject)

      if current_u.auth == 0:
        group = 'admin'
      elif current_u.auth == 1:
        group = 'teacher'
      else:
        group = 'student'
      params = {
                  'logout':users.create_logout_url("/"),
                  'user':current_u,
                  'group':group,
                  'subject':subject,
      }
      self.render('account.html',**params)

    def post(self):
      msg='test'
      success = None
      user = users.get_current_user()
      current_u=db.GqlQuery('SELECT * FROM User WHERE user = :1', user).get()
      new_name = self.request.get('nickname')
      search = db.GqlQuery('SELECT * FROM User WHERE nickname = :1', new_name).get()
      if not search:
        current_u.nickname = new_name
        current_u.put()
        msg='Success:)'
        success = 0
      else:
        msg='Sorry, name already exist > <'
        success = 1

      if current_u.auth == 0:
        group = 'admin'
      elif current_u.auth == 1:
        group = 'teacher'
      else:
        group = 'student'
      params = {
                  'logout':users.create_logout_url("/"),
                  'user':current_u,
                  'group':group,
                  'message':msg,
                  'success':success,
      }
      self.render('account.html',**params)


class EditPost(BaseHandler):
    def get(self):
      self.render('edit.html')

class Admin(BaseHandler):
    def get(self):
      self.render('admin.html')

class SubChoose(BaseHandler):
    def get(self):

      self.render('choose.html')

    def post(self):
      subject = self.request.get_all('subject')
      user = users.get_current_user()
      u=db.GqlQuery('SELECT * FROM User WHERE user = :1', user).get()
      u.subcombi = subject
      u.put()
      self.redirect('/main/account')

app = webapp2.WSGIApplication([('/', Login),
                               ('/main', MainPage),
                               ('/main/subject/(.*)', Subject),
                               ('/main/add_post',AddPost),
                               ('/main/post/(.*)',SinglePost),
                               ('/main/profile/(.*)',Profile),
                               ('/main/account', Account),
                               ('/main/edit_post', EditPost),
                               ('/main/subchoose', SubChoose),
                               ('/admin',Admin),                               
                              ],
                              debug=True)

'''
 
                                                             ('/main/singlepost', Singlepost),
                                                             ('/main/profile', Profile),
                                                             ('/main/postmodify', PostModify),
                                                             ('/main/profilemodify',ProfileModify),
'''