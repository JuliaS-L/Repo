#Home & info & contact
from julia_blog import db,mail
from flask import render_template, request, Blueprint,redirect,url_for
from julia_blog.models import BlogPost,Project
from julia_blog.core.forms import ContactForm
from flask_mail import Message

core=Blueprint('core',__name__)

@core.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)
    project_list = Project.query.order_by(Project.project_date.desc()).paginate(page=page,per_page=5)
    return render_template('index.html', posts=posts , projects= project_list)

@core.route('/info')
def info():
    return render_template('info.html')


@core.route('/contact',methods=['GET','POST'])
def contact():
    form = ContactForm()
    if form.is_submitted():
            mess = form.contact_text.data
            email = form.email.data
            msg = Message(mess,
                          sender=("MyWebsite", email),
                          recipients=["julia.schmidt-lademann@ism-student.de"])
            mail.send(msg)
            return redirect(url_for('core.index'))
    return render_template('contact.html')

