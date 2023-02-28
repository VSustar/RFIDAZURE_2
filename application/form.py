from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField,SubmitField
from wtforms.fields import DateField
from wtforms.validators import DataRequired
from datetime import datetime, date, timedelta


class DateInputForm(FlaskForm):
    today = date.today()
    sevendaysago = date.today() - timedelta(days = 7)
    date=DateField('startdate', format='%Y-%m-%d')
    startdate = DateField('Start Date', format='%Y-%m-%d',default=sevendaysago)
    enddate = DateField('End Date', format='%Y-%m-%d', default = today)
    submit = SubmitField('Submit')


  

                            
