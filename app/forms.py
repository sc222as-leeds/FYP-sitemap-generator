from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired, Length

class WebsiteForm(FlaskForm):
    url = StringField('Enter Website URL', validators=[DataRequired(), Length(0, 40)])
    submit = SubmitField('Run')