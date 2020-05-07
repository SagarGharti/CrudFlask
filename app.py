from flask import Flask, render_template, request, redirect, url_for, flash
# from sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
import csv


app = Flask(__name__)
app.secret_key = "Secret Key"

#sqlalchemy database configuration with mysql

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
#create model
class Data(db.Model):
      id= db.Column(db.Integer, primary_key = True)
      name= db.Column(db.String(100))
      email = db.Column(db.String(100))
      phone = db.Column(db.String(100))

      def __init__(self,name,email,phone):
          self.name = name
          self.email = email
          self.phone = phone
@app.route('/')
def index():
    all_data = Data.query.all()
    return render_template('index.html', employees = all_data)

@app.route('/employe')
def employe():
    return render_template('employe.html')    

@app.route('/post', methods =['POST']) 
def post():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        insert = Data(name,email,phone)
        db.session.add(insert)
        db.session.commit()
        #store books
        file = open("data.csv","a")
        writer = csv.writer(file)
        writer.writerow((name,email,phone))
        file.close()   
        #get all data
        flash("Employee insert sucessfully")
        return redirect(url_for('index'))

@app.route('/update/<id>/',methods=['GET','POST'])
def update(id):
    data = Data.query.filter_by(id = id)
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))
        # data.id = request.form['id']
        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']
        db.session.commit()
        flash("employee updated succesfully")
        return redirect(url_for('index'))
    if request.method == 'GET':
        return render_template('update.html', row = data)    

@app.route('/delete/<id>/', methods = ['GET','POST'])
def delete(id):
    data = Data.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/employe")
def read_employe():
    with open("data.csv","r") as file:
        reader = csv.reader(file)
        employe = list(reader)
    return render_template('index.html', employees = employe)      

if __name__ == '__main__':
    app.run(debug =True)    