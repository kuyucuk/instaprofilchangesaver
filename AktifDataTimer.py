from calistir import calistir
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import time

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class ReusableForm(Form):
    name = TextField('İsim:', validators=[validators.required()])
    mail = TextField("Email: ", validators=[validators.required()])

@app.route("/", methods=['GET', 'POST'])

def hello():
    form = ReusableForm(request.form)

    print
    form.errors
    if request.method == 'POST':
        name = request.form['name']
        mail = request.form['mail']

        if form.validate():
            # Save the comment here.
            if request.form.get('boxtitle') == request.form.get('boxh1') == request.form.get('boxh2')== request.form.get('boxbody') == None:
                flash("En az bir seçim yapmak zorundasınız! ")
            else:
                calistir(name, mail)
        else:
            flash('Tüm formlar doldurulmalıdır! ')



    return render_template('hello.html', form=form)

if __name__ == "__main__":
    app.run()







