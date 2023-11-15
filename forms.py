from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class AddForm(FlaskForm):
    name = StringField('Name of the Puppy: ', validators=[DataRequired()])
    breed = StringField('Breed of the Puppy: ', validators=[DataRequired()])
    submit = SubmitField('Add Puppy')


class DelForm(FlaskForm):
    id = IntegerField("ID Number of the puppy to be deleted: ", validators=[DataRequired()])
    submit = SubmitField('Remove Puppy')


class AddOwner(FlaskForm):
    pup_id = IntegerField("ID of the Puppy", validators=[DataRequired()])
    owner_name = StringField("Name of the Owner", validators=[DataRequired()])
    submit = SubmitField("Add Owner")
