from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange


class BookSearchForm(FlaskForm):
    query = StringField('Search by Title or Author', validators=[DataRequired()])
    submit = SubmitField('Search')


class BookEntryForm(FlaskForm):
    status = SelectField(
        'Status',
        choices=[('to-read', 'To Read'), ('reading', 'Reading'), ('finished', 'Finished')],
        default='to-read',
    )
    rating = IntegerField('Rating (1–5)', validators=[Optional(), NumberRange(min=1, max=5)])
    notes = TextAreaField('Notes', validators=[Optional()])
    submit = SubmitField('Save')