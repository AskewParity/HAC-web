from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DecimalField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class HAC_login(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    submit = SubmitField('Login')


class final_grade(FlaskForm):
    current_grade = DecimalField("Semester Grade", validators=[DataRequired()])
    desired_grade = DecimalField("Desired Grade", validators=[DataRequired()])
    weight = DecimalField("Weight of Final (XX%)", validators=[DataRequired()])

    submit = SubmitField('Submit')

class add_grade(FlaskForm):
    grade = DecimalField("Grade to Add", validators=[DataRequired()])
    category = SelectField("Type of Grade to Add", coerce=str,validators=[DataRequired()])

    submit = SubmitField('Submit')

class grade_goal(FlaskForm):
    goal = DecimalField("Grade Goal", validators=[DataRequired()])
    category = SelectField("Type of Grade to Change", coerce=str,validators=[DataRequired()])

    submit = SubmitField('Submit')