from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///atolye.db'
app.config['SECRET_KEY'] = "kapsulatolye"

db = SQLAlchemy(app)

class atolye(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   date_created = db.Column(db.DateTime, default = datetime.utcnow)
   equipment = db.Column(db.String(200))
   quantity = db.Column(db.String(5))
   staff = db.Column(db.String(50)) 
   team_name = db.Column(db.String(100))


def __init__(self, equipment, quantity, staff, team_name):
   self.equipment = equipment
   self.quantity = quantity
   self.staff = staff
   self.team_name = team_name

@app.route('/',methods=["POST", "GET"])
def index():
   if request.method == 'POST':
      if not request.form['equipment'] or not request.form['quantity'] or not request.form['staff'] or not request.form["team_name"]:
         flash('Please enter all the fields', 'error')
      else:
         borrow = atolye( equipment = request.form['equipment'], quantity = request.form['quantity'],
           staff = request.form['staff'], team_name =  request.form['team_name'])
         
         db.session.add(borrow)
         db.session.commit()
         flash('Record was successfully added')
         return redirect('/')
         
   borrows = atolye.query.order_by(atolye.date_created).all()  
   return render_template('index.html', borrows = borrows)

@app.route("/delete/<int:id>")
def delete(id):
    item_to_delete = atolye.query.get_or_404(id)

    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "There was a problem deleting that borrow"

@app.route("/update/<int:id>", methods = ["GET", "POST"])
def update(id):
    borrow = atolye.query.get_or_404(id)
    if request.method == "POST":
        borrow.equipment = request.form["equipment"]
        borrow.quantity = request.form["quantity"]
        borrow.staff = request.form["staff"]
        borrow.team_name = request.form["team_name"]
        
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue updating your borrow"

    else:
         return render_template("update.html", borrow = borrow)  

if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)