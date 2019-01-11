from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length

class ItemForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    select = SelectField('Select', choices=[('Soccer', 'Soccer'), ('Basketball', 'Basketball'),
                            ('Baseball', 'Baseball'), ('Frisbee', 'Frisbee'), 
                            ('Snowboarding', 'Snowboarding'), ('Rockclimbing', 'Rockclimbing'),
                            ('Football', 'Football'), ('Skating', 'Skating'),
                            ('Hockey', 'Hockey')])
    submit = SubmitField('Submit')
    