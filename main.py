from flask import Flask, abort, jsonify, make_response, redirect, render_template, request
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from data import db_session
from api import jobs_api
from api import users_api
from data.departments import Department
from data.jobs import Jobs
from data.users import User
from forms.departments import DepartmentForm
from forms.job import JobForm
from forms.login import LoginForm
from forms.register import RegisterForm
from map import getMapUrlByGeocode

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/mars_explorer.db")
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    app.run()


@app.errorhandler(404)
def not_found(error):
    if (request.path.startswith("/api/")):
        return make_response(jsonify({'error': 'Not found'}), 404)
    else:
        return render_template("error.html", title="404", text="Page not found"), 404


@app.errorhandler(500)
def internal_server_error(error):
    if (request.path.startswith("/api/")):
        return make_response(jsonify({'error': 'Internal Server Error'}), 500)
    else:
        return render_template("error.html", title="500", text="Internal Server Error"), 500


@app.errorhandler(401)
def unauthorized(error):
    if (request.path.startswith("/api/")):
        return make_response(jsonify({'error': 'Unauthorized'}), 401)
    else:
        return redirect("/login")


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
    return render_template('editForm.html', title='Registration', form=form)


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
    form = JobForm().init()
    if form.validate_on_submit():
        job = Jobs(
            job=form.job.data,
            team_leader=form.team_leader.data,
            work_size=form.work_size.data,
            collaborators=",".join(map(str, form.collaborators.data)),
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            is_finished=form.is_finished.data,
        )
        db_sess = db_session.create_session()
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('editForm.html', title='Adding a Job', form=form)


@app.route("/editjob/<int:id>", methods=['GET', 'POST'])
@login_required
def editjob(id):
    form = JobForm().init()
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == id, (Jobs.team_leader == current_user.id) | (current_user.id == 1)).first()
    if (not job):
        abort(404)
    if request.method == "GET":
        form.job.data = job.job
        form.team_leader.data = job.team_leader
        form.work_size.data = job.work_size
        form.collaborators.data = list(map(int, job.collaborators.split(",")))
        form.start_date.data = job.start_date
        form.end_date.data = job.end_date
        form.is_finished.data = job.is_finished
    if form.validate_on_submit():
        job.job = form.job.data
        job.team_leader = form.team_leader.data
        job.work_size = form.work_size.data
        job.collaborators = ",".join(map(str, form.collaborators.data))
        job.start_date = form.start_date.data
        job.end_date = form.end_date.data
        job.is_finished = form.is_finished.data
        db_sess.commit()
        return redirect('/')
    return render_template('editForm.html', title='Editing a Job', form=form)


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



@app.route("/departments")
def departments():
    session = db_session.create_session()
    departments = session.query(Department).all()
    return render_template("departments.html", title="List of Departments", departments=departments)


@app.route("/add_department", methods=['GET', 'POST'])
@login_required
def add_departments():
    form = DepartmentForm().init()
    if form.validate_on_submit():
        department = Department(
            title=form.title.data,
            chief=form.chief.data,
            members=",".join(map(str, form.members.data)),
            email=form.email.data,
        )
        db_sess = db_session.create_session()
        db_sess.add(department)
        db_sess.commit()
        return redirect('/departments')
    return render_template('editForm.html', title='Adding a Department', form=form)


@app.route("/edit_department/<int:id>", methods=['GET', 'POST'])
@login_required
def edit_departments(id):
    form = DepartmentForm().init()
    db_sess = db_session.create_session()
    department = db_sess.query(Department).filter(Department.id == id, (Department.chief == current_user.id) | (current_user.id == 1)).first()
    if (not department):
        abort(404)
    if request.method == "GET":
        form.title.data = department.title
        form.chief.data = department.chief
        form.members.data = list(map(int, department.members.split(",")))
        form.email.data = department.email
    if form.validate_on_submit():
        department.title = form.title.data
        department.chief = form.chief.data
        department.email = form.email.data
        department.members = ",".join(map(str, form.members.data))
        db_sess.commit()
        return redirect('/departments')
    return render_template('editForm.html', title='Editing a Department', form=form)


@app.route('/delete_department/<int:id>')
@login_required
def delete_departments(id):
    db_sess = db_session.create_session()
    department = db_sess.query(Department).filter(Department.id == id, (Department.chief == current_user.id) | (current_user.id == 1)).first()
    if department:
        db_sess.delete(department)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/departments')


@app.route("/users_show/<int:user_id>")
def users_show(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if (not user):
        abort(404)
    img = getMapUrlByGeocode(user.city_from)
    return render_template("users_show.html", title="Hometown", user=user, img=img)


if __name__ == '__main__':
    main()
