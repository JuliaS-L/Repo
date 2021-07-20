from flask import render_template,url_for,flash,redirect,request,Blueprint
from julia_blog import db
from flask_login import current_user,login_required
from julia_blog.models import BlogPost
from julia_blog.blog_posts.forms import BlogPostForm


blog_posts = Blueprint('blog_posts',__name__)


# @blog_posts.route("/blog/view")
# def posts():
#     page = request.args.get('page', 1, type=int)
#     #user = User.query.filter_by(username=username).first_or_404()
#     blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)
#     return render_template('blog_posts.html', blog_posts=blog_posts)

@blog_posts.route("/blog/create",methods=['GET','POST'])
@login_required
def create_post():
    form=BlogPostForm()
    if form.is_submitted():
        blog_post = BlogPost(blog_title=form.blog_title.data,
                            blog_text = form.blog_text.data,
                            user_id = current_user.id)
        db.session.add(blog_post)
        db.session.commit()
        flash('Blog Post Created')
##        this redirect should be changed to view the blog posts
##        the form should also have a picture upload function, not default always
        return redirect(url_for('core.index'))
    return render_template('create_post.html', form=form)

@blog_posts.route('/blog/<int:blog_post_id>')
def blog_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    return render_template('blog_post.html',
                            title=blog_post.blog_title,
                            text=blog_post.blog_text,
                            date = blog_post.date,
                            post=blog_post)


@blog_posts.route('/blog')
def blog_post_list():
    page = request.args.get('page',1,type=int)
    posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page,per_page=5)
    return render_template('blog_posts.html', posts=posts)



@blog_posts.route("/blog/<int:blog_post_id>/update",methods=['GET','POST'])
@login_required
def update_blog(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)
    form=BlogPostForm()
    if form.is_submitted():
        blog_post.blog_title = form.blog_title.data
        blog_post.blog_text = form.blog_text.data
#allow picture update
        db.session.commit()
        flash('Blog Post Updated')
##        this redirect should be changed to view the blog posts
##        the form should also have a picture upload function, not default always
        return redirect(url_for('blog_posts.blog_post',blog_post_id=blog_post.id))
    elif request.method == 'GET':
        form.blog_title.data = blog_post.blog_title
        form.blog_text.data = blog_post.blog_text
    return render_template('create_post.html', title='Updating',form=form)


@blog_posts.route("/blog/<int:blog_post_id>/delete",methods=['GET','POST'])
@login_required

def delete_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)

    if blog_post.author != current_user:
        abort(403)
    db.session.delete(blog_post)
    db.session.commit()
    flash('Blog post deleted')
    return redirect(url_for('core.index'))
