from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class TableForm(FlaskForm):
    """
    Form for editing/adding dining tables
    """
    name = StringField('Name', validators=[DataRequired()])
    catalog_no = StringField('Catalog No.', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    length = StringField('Length', validators=[DataRequired()])
    width = StringField('Width', validators=[DataRequired()])
    height = StringField('Height', validators=[DataRequired()])
    color = StringField('Color', validators=[DataRequired()])
    chair_count = StringField('Chair count', validators=[DataRequired()])
    chair_color = StringField('Chair color', validators=[DataRequired()])
    chair_height = StringField('Chair height', validators=[])
    chair_length = StringField('Chair length', validators=[])
    chair_width = StringField('Chair width', validators=[])
    image = FileField('Image', validators=[FileRequired()])
    submit = SubmitField('Submit', validators=[DataRequired()])
