from flask import Flask, render_template,redirect ,url_for,request ,flash
from flask_sqlalchemy import SQLAlchemy
import secrets

secret_key = secrets.token_hex(16)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
# example output, secret_key = 000d88cd9d90036ebdd237eb6b0db000
app.config['SECRET_KEY'] = secret_key
db = SQLAlchemy(app)

@app.route('/')
def index():
    new_list = List.query.all()
    person = Person.query.all()
    return render_template('base.html',new_list=new_list,person=person)

@app.route('/update/<int:item_id>')
def update_page(item_id):
    print(item_id)
    new_list = List.query.filter_by(id=item_id).all()
    return render_template('update.html',item=new_list)

    
class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(100),nullable=False)
    price = db.Column(db.Float,nullable=False)
    Quantity = db.Column(db.Integer,nullable=False)
    itp = db.Column(db.Float,nullable=False)

class Person(db.Model):
    name = db.Column(db.String(100),primary_key=True)
    bill = db.Column(db.Float,nullable=False,default=0)
    items = db.Column(db.Integer, db.ForeignKey('list.id'))
    list = db.relationship('List', backref='person', lazy=True)

@app.route("/add", methods=["POST"])
def add():
    # add new item
    item = request.form.get("item")
    price = float(request.form.get("price"))
    Quantity = float(request.form.get("Quantity"))
    itp = float(price*Quantity)
    new_list = List(item=item ,price=price ,Quantity=Quantity,itp=itp)
    db.session.add(new_list)
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/update/<int:item_id>', methods = ['GET', 'POST'])
def update(item_id):
    #if request.method == ['post']:
    list = List.query.filter_by(id=item_id).first()
    list.item = request.form.get('item')
    list.price = float(request.form.get('price'))
    list.Quantity = float(request.form.get('Quantity'))
    list.itp = list.Quantity*list.price
    db.session.commit()
    flash("Item Updated Successfully")
    return redirect(url_for("index"))

@app.route("/delete/<int:item_id>")
def delete(item_id):
    # delete item
    list = List.query.filter_by(id=item_id).first()
    db.session.delete(list)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)