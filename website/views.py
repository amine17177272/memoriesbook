from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Memorie, Comment, Like
from . import db

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    posts = Memorie.query.order_by(Memorie.date.desc()).all()
    return render_template('home.html', user=current_user, posts=posts)

@views.route('/main')
@login_required
def main():
    return render_template('index.html', user=current_user)

@views.route('/add-post', methods=['POST'])
@login_required
def add_post():
    content = request.form.get('content')

    if not content:
        flash('Post cannot be empty', category='error')
    else:
        new_post = Memorie(data=content, user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        flash('Post added!', category='success')

    return redirect(url_for('views.home'))

@views.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    content = request.form.get('content')

    if not content:
        flash('Comment cannot be empty', category='error')
    else:
        new_comment = Comment(content=content, post_id=post_id, user_id=current_user.id)
        db.session.add(new_comment)
        db.session.commit()
        flash('Comment added!', category='success')

    return redirect(url_for('views.home'))

@views.route('/post/<int:post_id>/like', methods=['POST'])
@login_required
def like_post(post_id):
    post = Memorie.query.get_or_404(post_id)
    like = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()

    if like:
        db.session.delete(like)
        db.session.commit()
        flash('Like removed!', category='success')
    else:
        new_like = Like(user_id=current_user.id, post_id=post_id)
        db.session.add(new_like)
        db.session.commit()
        flash('Post liked!', category='success')

    return redirect(url_for('views.home'))
