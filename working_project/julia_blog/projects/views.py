from flask import render_template,url_for,flash,redirect,request,Blueprint
from julia_blog import db
from flask_login import current_user,login_required
from julia_blog.models import User,BlogPost,Project
from julia_blog.projects.forms import ProjectForm


projects = Blueprint('projects',__name__)


@projects.route('/project/create',methods=['GET','POST'])
@login_required
def create_project():
    form = ProjectForm()
    if form.is_submitted():
        project = Project(project_title=form.project_title.data,
                        project_description = form.project_description.data,
                        project_text = form.project_text.data,
                        project_code = form.project_code.data,
                        project_github_code = form.project_github_code.data,
                        project_trinket_code = form.project_trinket_code.data,
                        user_id = current_user.id
                          )
        db.session.add(project)
        db.session.commit()
        flash('Project Created')
        return redirect(url_for('core.index'))
    return render_template('create_project.html',form=form)


@projects.route('/project/<int:project_id>')
def project(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('project.html',
                            project_title=project.project_title,
                            project_description=project.project_description,
                            project_text=project.project_text,
                            project_code=project.project_code,
                            project_trinket_code=project.project_trinket_code,
                            project_github_code=project.project_github_code,
                            project_date = project.project_date,
                            project=project)


@projects.route('/projects')
def project_list():
    page = request.args.get('page',1,type=int)
    project_list = Project.query.order_by(Project.project_date.desc()).paginate(page=page,per_page=5)
    return render_template('projects.html',
                            project_list=project_list)



@projects.route("/project/<int:project_id>/update",methods=['GET','POST'])
@login_required
def update(project_id):
    project = Project.query.get_or_404(project_id)
    if project.author != current_user:
        abort(403)
    form=ProjectForm()
    if form.is_submitted():
        project.project_title = form.project_title.data
        project.project_description = form.project_description.data
        project.project_text = form.project_text.data
        project.project_code = form.project_code.data
        project_trinket_code = form.project_trinket_code
        project_github_code = form.project_github_code
#allow picture update
        db.session.commit()
        flash('Project Updated')
##        this redirect should be changed to view the blog posts
##        the form should also have a picture upload function, not default always
        return redirect(url_for('project/projects.project',project_id=project.id))
    elif request.method == 'GET':
        form.project_title.data = project.project_title
        form.project_description.data = project.project_description
        form.project_text.data = project.project_text
        form.project_code.data = project.project_code
        form.project_github_code.data = project.project_github_code
        form.project_trinket_code.data = project.project_trinket_code
    return render_template('create_project.html', title='Updating',form=form)




@projects.route("/project/<int:project_id>/delete",methods=['GET','POST'])
@login_required

def delete_project(project_id):
    project = Project.query.get_or_404(project_id)

    if project.author != current_user:
        abort(403)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted')
    return redirect(url_for('core.index'))
