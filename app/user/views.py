import json
from flask import jsonify, render_template, request

from . import user
from ..models import Table

@user.route('/')
def homepage():
    """
    Default route
    """
    return render_template('user/home.html', title="Welcome!")

@user.route('/catalog')
def view_catalog():
    """
    Gets item data to display
    """
    tables = Table.get_tables()

    return render_template('user/catalog.html', tables=tables, title="Catalog")

@user.route('/api-search', methods=['POST'])
def search_catalog():
    """
    Searches catalog for items matching user's input from catalog search form
    """
    #turns JSON string from jQuery to python dict
    searchObj = json.loads(request.data)

    found_tables = Table.search_tables(searchObj)
    return jsonify(found_tables)
