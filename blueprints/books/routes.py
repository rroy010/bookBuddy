from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from bson.objectid import ObjectId
import requests

from . import books_bp
from .forms import BookSearchForm, BookEntryForm
from .utils import search_google_books
from models import mongo


@books_bp.route('/search', methods=['GET', 'POST'])
def search():
    form = BookSearchForm()
    results = []
    if form.validate_on_submit():
        results = search_google_books(form.query.data)
    return render_template('search.html', form=form, results=results)


@books_bp.route('/bookshelf')
@login_required
def bookshelf():
    entries = list(mongo.db.bookshelf.find({'user_id': current_user.id}))
    return render_template('bookshelf.html', books=entries)


@books_bp.route('/book/add/<volume_id>', methods=['GET', 'POST'])
@login_required
def add_book(volume_id):
    form = BookEntryForm()
    if form.validate_on_submit():
        title = ''
        authors = []
        thumbnail = ''
        try:
            resp = requests.get(f'https://www.googleapis.com/books/v1/volumes/{volume_id}', timeout=5)
            if resp.ok:
                info = resp.json().get('volumeInfo', {})
                title = info.get('title', '')
                authors = info.get('authors', [])
                thumbnail = info.get('imageLinks', {}).get('thumbnail', '')
        except Exception:
            pass

        mongo.db.bookshelf.insert_one(
            {
                'user_id': current_user.id,
                'volume_id': volume_id,
                'title': title,
                'authors': authors,
                'thumbnail': thumbnail,
                'status': form.status.data,
                'rating': form.rating.data,
                'notes': form.notes.data,
            }
        )
        flash('Book saved to your bookshelf!', 'success')
        return redirect(url_for('books.bookshelf'))
    return render_template('add_book.html', form=form)


@books_bp.route('/book/delete/<entry_id>', methods=['POST'])
@login_required
def delete_book(entry_id):
    try:
        mongo.db.bookshelf.delete_one({'_id': ObjectId(entry_id), 'user_id': current_user.id})
        flash('Book removed.', 'info')
    except Exception:
        flash('Unable to delete the book.', 'danger')
    return redirect(url_for('books.bookshelf'))


@books_bp.route('/book/edit/<entry_id>', methods=['GET', 'POST'])
@login_required
def edit_book(entry_id):
    # Find the existing entry for this user
    entry = mongo.db.bookshelf.find_one({'_id': ObjectId(entry_id), 'user_id': current_user.id})
    if not entry:
        flash('Book not found.', 'danger')
        return redirect(url_for('books.bookshelf'))

    form = BookEntryForm(status=entry.get('status'), rating=entry.get('rating'), notes=entry.get('notes'))
    if form.validate_on_submit():
        mongo.db.bookshelf.update_one(
            {'_id': entry['_id'], 'user_id': current_user.id},
            {
                '$set': {
                    'status': form.status.data,
                    'rating': form.rating.data,
                    'notes': form.notes.data,
                }
            },
        )
        flash('Book updated.', 'success')
        return redirect(url_for('books.bookshelf'))
    return render_template('edit_book.html', form=form, entry=entry)