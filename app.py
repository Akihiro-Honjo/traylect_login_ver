from flask import Flask
from flask import render_template,g,redirect,request
import sqlite3
DATABASE="memo.db"
from flask_login import UserMixin,LoginManager,login_required,login_user,logout_user
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self,userid):
        self.id = userid

# ログイン
@login_manager.user_loader
def load_user(userid):
    return User(userid)
@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login')

@app.route("/logout",methods=['GET'])
def logout():
    logout_user()
    return redirect('/login')

@app.route("/login",methods=['GET','POST'])
def login():
    error_message = ''
    userid = ''
    
    if request.method == 'POST':
        userid = request.form.get('userid')
        password = request.form.get('password')
        #ログインチェック
        if(userid == 'test' and password == 'password'):
            user = User(userid)
            login_user(user)
            return redirect('/')
        else:
            error_message ='入力されたIDもしくはパスワードが誤ってます'
        
    return render_template('login.html',userid=userid,error_message=error_message)
    

# todo_list = [
#     {'title':"test1", 'body':"flask"},
#     {'title':"test2", 'body':"python"},
#     {'title':"test3", 'body':"ChatGPT"}
# ]

@app.route('/')
@login_required
def index():
    todo_list = get_db().execute("select id,title,body from todo").fetchall()
    
    return render_template('index.html',todo_list=todo_list)

@app.route("/regist",methods=['GET','POST'])
@login_required
def regist():
    if request.method =='POST':
        # 画面からの登録情報
        title = request.form.get('title')
        body = request.form.get('body')
        db = get_db()
        db.execute("insert into todo (title,body) values(?,?)",[title,body])
        db.commit()
        return redirect('/')
    return render_template('regist.html')

# database接続
def connect_db():
    rv = sqlite3.connect(DATABASE)
    rv.row_factory = sqlite3.Row
    return rv
def get_db():
    if not hasattr(g,'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db