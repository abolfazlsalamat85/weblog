from flask import Flask , render_template, redirect , session , request
from app.databaseNoSQL import *
from datetime import timedelta

app = Flask(__name__)
app.secret_key='klasjf;lksa ;lkjallk=sakl;lf654-655 65464'
app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/blog0410'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=25)
init_db(app)

@app.route("/")
def home_page():
    return render_template('index.html',posts=get_posts())

@app.route("/login",methods=['POST','GET'])
def login():
    session.setdefault('counter',3)
    if session.get('counter'):
        if request.method == 'POST':
            session['counter'] -= 1
            myUser = request.form['username']
            myPassword=request.form['password']
            if myUser=='Abolfazl' and myPassword == '1975':
                #save log
                session['user_name']='Kambiz'
                session['is_login']=True
                return redirect('/')
            else:
                #save invalid log
                return render_template('login.html',msg=f'Invalid Username or Password\nu can try {session['counter']} more times! ')
    else:
        return render_template('login.html',msg=f'u r banned')
    return render_template('login.html')

@app.route("/newpost",methods=['POST','GET'])
def new_post():
    import os
    from time import time
    if not session.get('is_login'):
        return redirect('/login')
    if request.method == 'POST':
        myTitle=request.form['title']
        myContent=request.form['content']
        myImage=None
        if 'image' in request.files and request.files['image'].filename != '':
            file = request.files['image']
            filename=f'{time()}_{file.filename}'
            filePath=os.path.join('static','uploads','image',filename)
            file.save(filePath)
            myImage=filename

        add_post(myTitle,myContent,myImage)
        return redirect('/')
    return render_template('newpost.html')

@app.post('/post/<int:post_id>')
def delete_post(post_id):
    delete_post_from_db(post_id)
    return redirect('/')

@app.route("/logout")
def logout():
    session.pop('user_name')
    session.pop('is_login')
    return redirect('/')

@app.route("/comments/<int:post_id>",methods=['POST','GET'])
def comments(post_id):
    post=get_post_by_id(post_id)
    if request.method=='POST':
        author=request.form['author']
        text=request.form['text']
        if author == '':
            return render_template('comments.html',post = post,msg='Enter ur name!')
        if text == '':
            return render_template('comments.html',post = post,msg='Enter ur Comment!')
        add_comment(post_id,author,text)
        return redirect(f"/comments/{post_id}")
    else:
        return render_template('comments.html',post = post)

@app.post("/comments/<int:post_id>/<int:comment_index>")
def change_comment_status(post_id,comment_index):
    button=request.form['but']
    if button == 'Delete Comment':
        delete_comment_from_db(post_id,comment_index)
    else:
        update_comment_status(post_id,comment_index)
    return redirect(f"/comments/{post_id}")



if __name__ == '__main__':
    app.run(  )