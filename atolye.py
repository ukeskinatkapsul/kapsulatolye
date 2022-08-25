from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///borrow.db"
db = SQLAlchemy(app)

class atolye(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    equipment = db.Column(db.String(100), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    quantity = db.Column(db.Integer)
    staff = db.Column(db.String(30), nullable = False)
    team_name = db.Column(db.String(100), nullable = False)


    def __repr__(self):
        return "<Task %r>" % self.id
       

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        borrow_equipment = request.form["equipment"]
        new_equipment = atolye(equipment=borrow_equipment)

        borrow_quantity = request.form["quantity"]
        new_quantity = atolye(quantity=borrow_quantity)
        
        borrow_staff = request.form["staff"]
        new_staff = atolye(quantity=borrow_staff)
        
        borrow_team_name = request.form["team_name"]
        new_team_name = atolye(quantity=borrow_team_name)


        try:
            db.session.add(new_equipment, new_quantity, new_staff, new_team_name) #new_task, bunu kaldırınca niye tarih çalışıyor???
            #db.session.add(new_deadline)
            db.session.commit()
            return redirect("/")
        except:
            return "There is an issue adding your task"

    else:
        borrows = atolye.query.order_by(atolye.date_created).all()
        return render_template("index.html", borrows = borrows)


@app.route("/delete/<int:id>")
def delete(id):
    item_to_delete = atolye.query.get_or_404(id)

    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "There was a problem deleting that task"

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
            return "There was an issue updating your task"

    else:
         return render_template("update.html", borrow = borrow)  


if __name__ == "__main__":
    app.run(debug=True)
