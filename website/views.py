from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Memorie, Comment, User, Like
from . import db

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template('home.html', user=current_user)

@views.route('/main')
@login_required
def main():
    posts = Memorie.query.all()
    return render_template('index.html', user=current_user, posts=posts)

@views.route('/post', methods=['POST'])
@login_required
def add_post():
    content = request.form['content']
    new_post = Memorie(data=content, user_id=current_user.id)
    db.session.add(new_post)
    db.session.commit()
    return redirect(url_for('views.main'))

@views.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    post = Memorie.query.get_or_404(post_id)
    content = request.form['content']
    new_comment = Comment(content=content, post_id=post.id, user_id=current_user.id)
    db.session.add(new_comment)
    db.session.commit()
    return redirect(url_for('views.home'))

@views.route('/post/<int:post_id>/like', methods=['POST'])
@login_required
def like_post(post_id):
    post = Memorie.query.get_or_404(post_id)
    like = Like.query.filter_by(user_id=current_user.id, post_id=post.id).first()
    
    if like:
        db.session.delete(like)
        db.session.commit()
        status = 'unliked'
    else:
        new_like = Like(user_id=current_user.id, post_id=post.id)
        db.session.add(new_like)
        db.session.commit()
        status = 'liked'
    
    # Refresh the likes relationship to get the current count
    post = Memorie.query.get_or_404(post_id)
    like_count = len(post.likes)
    
    return jsonify({'status': status, 'like_count': like_count})
