from flask import Flask,render_template,request,redirect,url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///users.sqlite3"
db = SQLAlchemy(app)

class users(db.Model):
    id = db.Column("id",db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    task = db.Column(db.String(100))
    date = db.Column(db.String(100))
    enddate = db.Column(db.String(100))
    def __init__(self,task,date,name,enddate):
        self.task = task
        self.date=date
        self.name = name
        self.enddate =enddate
usernames=['']  
loggedin=[]

@app.route("/")
def mainpage():
    if loggedin:
        login = False
    else:
        login=True
    b = users.query.filter_by(name=usernames[0]).all()
    
    return render_template("page.html",content=b,login = login)



@app.route("/login",methods=['POST','GET'])
def login():
    username = request.form['user']
    usernames[0] = username
    loggedin.append(0)
    return redirect("/")


@app.route("/logout",methods=['POST','GET'])
def logout():
    loggedin.clear()
    return redirect("/")


@app.route("/schedule",methods=['POST','GET'])
def schedule():
    task = request.form['task']
    a = request.form['datee']
    
    
    a = users(task=task,date=datetime.today().date(),name=usernames[0],enddate=a)
    db.session.add(a) 
    db.session.commit()
    return redirect("/")

@app.route("/delete/<int:id>",methods=['POST','GET'])
def delete(id):
    
    task_to_delete = users.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        pass
    
    return redirect("/")









if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)