from flask import Flask, render_template
import pandas as pd

# Create Home Page Route
app = Flask(__name__)

app.config['SECRET_KEY'] = '***'


from application import routes
