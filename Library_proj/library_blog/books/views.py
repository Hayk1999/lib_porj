from os import abort
import flask_wtf


from flask import render_template, url_for, redirect, request, flash, Blueprint
from flask_login import current_user, login_required
from library_blog import db
from library_blog.models import Book
from library_blog.books.forms import BookForm

books = Blueprint('books', __name__)

#CREATE#
@books.route('/add', methods=["GET", "POST"])
@login_required
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        book = Book(title=form.title.data, description=form.description.data, author=form.author.data, cover=form.cover.data, user_id=current_user.id)
        db.session.add(books)
        db.session.commit
        flash("Book added")
        return redirect(url_for('core.index'))
    return render_template('add_book.html', form=form)

#READ#
@books.route('/<int:book_id>')
def book(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book.html', title=book.title, date=book.date)

#UPDATE#
@books.route('/<int:book_id>/update', methods=["GET", "POST"])
@login_required
def update(book_id):
    book = Book.query.get_or_404(book_id)
    if book.author != current_user:
        abort(403)
    form = BookForm()

    if form.validate_on_submit():
        book.title = form.title.data
        book.description = form.description.data
        book.author = form.author.data, 
        book.cover =form.cover.data
        db.session.commit
        flash("Book updated")
        return redirect(url_for('book.book', book_id=book_id))
    
    elif request.method == 'GET':
        form.title.data = book.title
        form.description.data = book.description
    
    return render_template('add_book.html', title='Updating', form=form)

#DELETE#
@books.route('/<int:book_id>/delete', methods=["GET", "POST"])
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.author != current_user:
        abort(403)
    
    db.session.delete(book)
    db.session.commit()
    flash('book deleted')
    return redirect(url_for('core.index'))

