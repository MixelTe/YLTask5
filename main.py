from flask import Flask, redirect, render_template
from data import db_session
from data.jobs import Jobs
from data.users import User
from forms.register import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/mars_explorer.db")
    app.run()


@app.route("/")
def index():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return render_template("index.html", title="Works log", jobs=jobs)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess = db_session.create_session()
        db_sess.add(user)
        db_sess.commit()
        return redirect('/register_success')
    return render_template('register.html', title='Registration', form=form)


@app.route("/register_success")
def register_success():
    return render_template('/register_success.html', title='Registration')


if __name__ == '__main__':
    main()
