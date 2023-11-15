import os
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from forms import AddForm, DelForm, AddOwner

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'my-key'

db = SQLAlchemy(app)
Migrate(app, db)


class Puppy(db.Model):
    __tablename__ = 'puppies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    breed = db.Column(db.Text)
    owner = db.relationship('Owner', backref='puppy', uselist=False, cascade='all, delete-orphan')

    def __init__(self, name: str, breed: str):
        self.name = name
        self.breed = breed

    def __repr__(self):
        curr_owner = Owner.query.filter_by(pup_id=self.id).first()
        if not curr_owner:
            return f"Puppy name: {self.name}, Breed: {self.breed}. Owner: None"
        else:
            return f"Puppy name: {self.name}, Breed: {self.breed}, Owner: {curr_owner.name}"


class Owner(db.Model):
    __tablename__ = 'owners'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    pup_id = db.Column(db.Integer, db.ForeignKey('puppies.id'))

    def __init__(self, name: str, pup_id: int):
        self.name = name
        self.pup_id = pup_id

    def __repr__(self):
        return f"Owner Name: {self.name}, Puppy ID: {self.pup_id}"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_pup', methods=['GET', 'POST'])
def add_pup():
    form = AddForm()
    if form.validate_on_submit():
        name = form.name.data
        breed = form.breed.data
        new_pup = Puppy(name=name, breed=breed)
        db.session.add(new_pup)
        db.session.commit()
        return redirect(url_for('list_pup'))
    return render_template('add_pup.html', form=form)


@app.route('/list_pup')
def list_pup():
    puppies = Puppy.query.all()
    return render_template('list_pup.html', puppies=puppies)


@app.route('/add_owner', methods=['GET', 'POST'])
def add_owner():
    form = AddOwner()
    if form.validate_on_submit():
        pup_id = form.pup_id.data
        owner_name = form.owner_name.data

        Puppy.query.get_or_404(pup_id,description=f"Puppy with ID : {pup_id}")

        # If Owner of Puppy already exists
        curr_owner = Owner.query.filter_by(pup_id=pup_id).first()
        if curr_owner:
            curr_owner.name = owner_name
            db.session.commit()
            return redirect(url_for('list_pup'))
        else:
            new_owner = Owner(name=owner_name, pup_id=pup_id)
            db.session.add(new_owner)

        db.session.commit()
        return redirect(url_for('list_pup'))

    return render_template('add_owner.html', form=form)


@app.route('/del_pup', methods=['GET', 'POST'])
def del_pup():
    form = DelForm()
    if form.validate_on_submit():
        del_id = form.id.data
        pup = Puppy.query.get_or_404(del_id,description=f"Puppy with ID : {del_id}")
        db.session.delete(pup)
        db.session.commit()
        return redirect(url_for('list_pup'))
    return render_template('del_pup.html', form=form)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
