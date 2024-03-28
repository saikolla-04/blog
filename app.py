from flask import Flask ,render_template,url_for,request,redirect,flash,session
import mysql.connector
app=Flask(__name__)
#secret key
app.config['SECRET_KEY']='my super secret key that no one is supposed to know'
mydb=mysql.connector.connect(host='localhost',user='root',password='system',db="blogsss54")
with mysql.connector.connect(host="localhost",password="system",user="root",db="blogsss54"):
    cursor=mydb.cursor(buffered=True)
    cursor.execute("create table if not exists registration54(username varchar(50) primary key,moblie varchar(20) unique,email varchar(50),address varchar(50), password varchar(20))")
    
mycursor=mydb.cursor()

@app.route('/form54',methods=['GET','POST'])  
def reg54():
    if request.method=="POST":
        username=request.form["username"]
        moblie=request.form["moblie"]
        email=request.form["email"]
        address=request.form["address"]
        password=request.form["password"]
        otp=genotp()
        sendmail(to=email,subject="Thanks for registration",body=f'otp is{otp}')
        return render_template("verification.html",username=username,moblie=moblie,email=email,address=address,password=password,otp=otp)
    return render_template("registration54.html")
@app.route('/otp/<username>/<moblie>/<email>/<address>/<password>/<otp>',methods=["GET","POST"])
def otp(username,moblie,email,address,password,otp):
    if request.method=="POST":
        uotp=request.form['uotp']
        print(uotp)
        if otp==uotp:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('insert into registration54 values(%s,%s,%s,%s,%s)',[username,moblie,email,address,password])
            mydb.commit()
            cursor.close()
            return "success"
            #return redirect(url_for("login"))
    return render_template("verification54.html",username=username,moblie=moblie,email=email,address=address,password=password,otp=otp)


@app.route('/login',methods=["GET","POST"])
def login():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        cursor=mydb.cursor(buffered=True)
        cursor.execute("select count(*) from registration54 where username=%s && password=%s",[username,password])
        data=cursor.fetchone()[0]
        if data==1:
            session['username']=username
            if not session.get(session['username']):
                session[session['username']]={}
            return redirect(url_for('homepage'))
        else:
            return 'Invalid Username and password'                                     
    return render_template("login.html")
@app.route('/logout')
def logout():
    if session.get('username'):
        session.pop('username')
    return redirect(url_for('login'))
@app.route('/')
def homepage():
    return render_template('homepage.html')
@app.route('/addpost',methods=['GET','POST'])
def add_post():
    if request.method=="POST":
        title=request.form['title']
        content=request.form['title']
        slug=request.form['slug']
        print(title)
        print(content)
        print(slug)
        cursor=mydb.cursor(buffered=True)
        cursor.execute('INSERT INTO posts(title,content,slug) VALUES (%s,%s,%s)',(title,content,slug))
        mydb.commit()
        cursor.close()
    return render_template('add_post.html')
#create admin page
@app.route('/admin')
def admin():
    return render_template('admin.html')
#View posts
@app.route('/viewposts',methods=['POST'])
def view_posts():
    cursor=mydb.cursor(buffered=True)
    cursor.execute("SELECT * FROM posts")
    posts=cursor.fetchall()
    print(posts)
    cursor.close()
    return render_template("viewposts.html",posts=posts)
#delete post route
@app.route('/delete_post',methods=['POST'])
def delete_post(id):
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select * from posts where id=%s',(id,))
    post=cursor.fetchone()
    cursor.execute('DELETE FROM posts WHERE id=%s',(id,))
    mydb.commit()
    cursor.close()

    return redirect(url_for('view_posts'))

app.run(debug=True,use_reloader=True)