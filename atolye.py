from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///atolye.db'
db = SQLAlchemy(app)

class atolye(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    equipment = db.Column(db.String(100))
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    quantity = db.Column(db.Integer)
    staff = db.Column(db.String(30))
    team_name = db.Column(db.String(100))


    def __init__(self, equipment, date_created, quantity, staff, team_name):
        self.equipment = equipment
        self.date_created = date_created
        self.quantity = quantity
        self.staff = staff
        self.team_name = team_name   

db.create_all()

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        equipment_content = request.form["equipment"]
        new_equipment = atolye(equipment=equipment_content)
        
        quantity_content = request.form["quantity"]
        new_quantity = atolye(quantity=quantity_content)
        
        staff_content = request.form["staff"]
        new_staff = atolye(staff=staff_content)
        
        team_name_content = request.form["team_name"]
        new_team_name = atolye(team_name=team_name_content)

        try:
            #db.session.add_all([new_equipment, new_quantity, new_staff, new_team_name])
            db.session.add(new_equipment)
            #db.session.add(new_team_name)
            #db.session.add(new_staff)
            #db.session.add(new_quantity) 
            db.session.commit()
            return redirect("/")
        except:
            return "There is an issue adding your borrow"

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


if __name__ == "__main__":
    app.run(debug=True)
