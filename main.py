from flask import Flask, abort, redirect, render_template, request
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from data import db_session
from data.jobs import Jobs
from data.users import User
from forms.job import JobForm
from forms.login import LoginForm
from forms.register import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/mars_explorer.db")
    app.run()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', title='Авторизация',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/addjob", methods=['GET', 'POST'])
@login_required
def addjob():
    form = JobForm()
    if form.validate_on_submit():
        job = Jobs(
            job=form.job.data,
            team_leader=form.team_leader.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            is_finished=form.is_finished.data,
        )
        db_sess = db_session.create_session()
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('editjob.html', title='Adding a Job', form=form)


@app.route("/editjob/<int:id>", methods=['GET', 'POST'])
@login_required
def editjob(id):
    form = JobForm()
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == id, (Jobs.team_leader == current_user.id) | (current_user.id == 1)).first()
    if (not job):
        abort(404)
    if request.method == "GET":
        form.job.data = job.job
        form.team_leader.data = job.team_leader
        form.work_size.data = job.work_size
        form.collaborators.data = job.collaborators
        form.start_date.data = job.start_date
        form.end_date.data = job.end_date
        form.is_finished.data = job.is_finished
    if form.validate_on_submit():
        job.job = form.job.data
        job.team_leader = form.team_leader.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.start_date = form.start_date.data
        job.end_date = form.end_date.data
        job.is_finished = form.is_finished.data
        db_sess.commit()
        return redirect('/')
    return render_template('editjob.html', title='Editing a Job', form=form)


@app.route('/deletejob/<int:id>')
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == id, (Jobs.team_leader == current_user.id) | (current_user.id == 1)).first()
    if job:
        db_sess.delete(job)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')



if __name__ == '__main__':
    main()
