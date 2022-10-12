from flask import Blueprint
from HAC_app import db
from flask import render_template, flash, redirect, url_for, request, session
from HAC_app.grades.forms import HAC_login, final_grade, add_grade, grade_goal
from HAC_app.models import User
from HAC_app.grades.utils import Access
from flask_login import login_user, current_user, logout_user, login_required
dic = {}

user = Blueprint('user', __name__)

@user.route('/login', methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('user.hac'))
    form = HAC_login()
    final_calc = final_grade()
    if final_calc.validate_on_submit():
        cg = float(final_calc.current_grade.data)
        dg = float(final_calc.desired_grade.data)
        w = float(final_calc.weight.data) / 100
        
        flash(f'Final Grade Needed -  {round((dg - cg * (1 - w)) / w, 2)}%', 'info')
    elif form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('user.hac'))
    
    return render_template('login.html', title='Login', form=form, final_calc=final_calc)

@user.route('/hac')
@login_required
def hac():
    try :
        grade_info = Access(current_user.username, current_user.password)
        if grade_info.info[0]:
            flash('You have been logged in!', 'success')
        else:
            flash('Login Unsuccessful. Could not connect to HAC | Try again', 'danger')
            return redirect(url_for('main.index'))
    except :
        flash('Login Unsuccessful. Could not connect to HAC | Try again', 'danger')
        return redirect(url_for('main.index'))
    return render_template('hac.html', title='hac', info=grade_info.info)

@user.route('/logout')
def logout():
    try:
        username = current_user.username
        logout_user()
        user = User.query.filter_by(username=username)
        for e in user:
            db.session.delete(e)
            db.session.commit()
        flash('Successfully logged out','success')
    except:
        flash('ERROR in logging out','danger')
    return redirect(url_for('main.index'))

@user.route('/hac/<int:course>', methods=['GET', 'POST'])
@login_required
def specific_course(course):
    add = add_grade()
    goal = grade_goal()
    grades = Access(current_user.username, current_user.password)
    grade_info = grades.info[int(course)]
    groups_list=[(i.type, i.type) for i in grade_info.grade_agg]
    add.category.choices = groups_list
    goal.category.choices = groups_list

    if add.validate_on_submit():
        add_G = float(add.grade.data)
        category = str(add.category.data)
        
        new_grade = grades.add_grade(add_G, course, category)
        flash(f'New Grade in {grade_info.title} : {round(sum([float(e.actual) for e in grade_info.grade_agg]) * 100 / sum(float(e.weight) for e in grade_info.grade_agg))}', 'info')
    if goal.validate_on_submit():
        goal_G = float(goal.goal.data)
        category = str(goal.category.data)

        needed = grades.grade_needed(goal_G, course, category)
        flash(f'Needed Grades {needed}','info')
        
    return render_template('course.html', title='Course', course=grade_info, add_form=add, goal_form=goal)