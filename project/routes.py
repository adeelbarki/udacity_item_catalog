from flask import render_template, url_for, flash, redirect, request
from project import app, db
from project.database_setup import Category, Item
from project.forms import ItemForm


@app.route("/")
@app.route("/catalog")
def catalog():
    categories = Category.query.all()
    items = Item.query.all()
    return render_template("catalog.html", categories=categories, items=items)


@app.route("/catalog/new", methods=['GET', 'POST'] )
def new_item():
    form = ItemForm()
    if form.validate_on_submit():
        category = Category.query.filter_by(name=form.select.data).first()
        item = Item(title=form.title.data, description=form.description.data, cat_id=category.id)
        db.session.add(item)
        db.session.commit()
        flash('Your item is added', 'success')
        return redirect(url_for('catalog'))
    return render_template('addNewItem.html', title='Add Item', form=form, legend='Add Item')


@app.route("/item/<item_id>/")
def item(item_id):
    item = Item.query.get_or_404(item_id)
    return render_template('item.html', title=item.title, item=item)


@app.route("/item/<item_id>/edit", methods=['GET', 'POST'])
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)
    category = Category.query.filter_by(id=item.cat_id).first()
    form = ItemForm()
    if form.validate_on_submit():
        item.title = form.title.data
        item.description = form.description.data
        category = Category.query.filter_by(name=form.select.data).first()
        item.cat_id = category.id
        db.session.commit()
        flash("Item has been edited")
        return redirect(url_for('item', item_id=item.id))
    elif request.method == 'GET':
        form.title.data = item.title
        form.description.data = item.description
        form.select.data = category.name
    return render_template('addNewItem.html', title='Edit Item', form=form, 
                                legend='Edit Item')