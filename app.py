from flask import Flask,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://divyanshu:software@localhost/tododb'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class todo(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    content = db.Column(db.String,nullable = False)
    is_done = db.Column(db.Boolean,default = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/',methods = ['POST','GET'])
def index():
    if request.method == 'POST':
        if len(request.form['content']) > 0:
            task_content = request.form['content']
            new_task = todo(content = task_content)
            
            try:
                db.session.add(new_task)
                db.session.commit()
                return redirect('/')
            except:
                return "Task is added " + task_content
        else:
            return "Empty taks can not be added"
    else:
        todos = todo.query.order_by(todo.date_created).all()
        return render_template('home.html', todos = todos)

@app.route('/delete/<int:id>' ,methods = ['POST','GET'])
def delete(id):
    task = todo.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
        return redirect('/')
    except:
        return "Sorry taks can not be deleted"


@app.route('/edit/<int:id>',methods = ['GET','POST'])
def editView(id):
    task = todo.query.get_or_404(id)
    if request.method == 'POST':    
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There is some Error"
    else:
        return render_template('editview.html',task = task)




if __name__  == "__main__":
    app.run(debug=True)