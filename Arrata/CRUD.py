import sqlite3
from . import database
from datetime import datetime


def modify_price(price):
    now = datetime.now().time()

    if 11 <= now.hour <= 13:
        return round(price * 1.10, 2)
    elif 18 <= now.hour <= 20:
        return round(price * 0.9, 2)
    else:
        return price

def get_menu(type:str):
    """
    Args:
        type: don, drinks or sashimi
    Returns: menu.html
    """
    db = database.get_db()
    items = db.execute(
        'SELECT id, item_name, item_price, item_picture_path'
        '   FROM menu'
        '   WHERE item_type=?',
        (type.upper(),)
    ).fetchall()

    for item in items:
        new_price = modify_price(item['item_price'])
        item['item_price'] = new_price

    return items

def update_cart(id: int, quantity: int, customer_id: int):
    """Update cart from add to cart
    Note: There should be another argument for customer id.
    Use customer id and the item id to find if the
    item already exists in the cart
    Note: item_total is total price of the item
    Args:
        id (int): item_menu_id
        quantity (int): old quantity + 1
        db (sqlite3.Connection): database connection object
    """
    db = database.get_db()
    db.execute(
        'UPDATE cart'
        '   SET item_quantity = ?, item_total = ?'
        '   WHERE customer_id = ?'
        '   AND item_menu_id = ?',
        (quantity, 1, customer_id, id)
    )
    db.commit()


def add_cart(id: int, quantity: int, customer_id: int):
    """Add to cart.
    Adds a new item to the cart
    Args:
        id (int): item_menu_id
        quantity (int): 1
        db (sqlite3.Connection): database connection object
    """
    db = database.get_db()
    db.execute(
        'INSERT INTO cart'
        '   (customer_id, item_menu_id, item_quantity, item_total, is_random)'
        '   VALUES'
        '   (?, ?, ?, ?, ?)',
        (customer_id, id, quantity, quantity, 0)
    )
    db.commit()


def find_cart(id: int, customer_id: int):
    """Finds the item with the item_menu_id
    Note: There should be another arg for customer id
    Args:
        id (int): [description]
        db (sqlite3.Connection): [description]
    Returns:_cart
        [type]: [description]
    """
    db = database.get_db()
    result = db.execute(
        'SELECT m.item_price, c.item_quantity'
        '    FROM menu m'
        '    INNER JOIN cart c'
        '    ON m.id = c.item_menu_id'
        '    WHERE c.item_menu_id = ?'
        '    AND c.customer_id = ?',
        (id, customer_id)
    ).fetchone()

    if result is not None:
        new_price = modify_price(result['item_price'])
        result['item_price'] = new_price

    return result

def get_cart(customer_id):
    """ Note: In the future add customer id as arg """
    db = database.get_db()
    bag = db.execute(
        # 'SELECT item_menu_id, item_quantity, item_total'
        # '   FROM cart'
        # '   WHERE customer_id=1'

        'SELECT m.id, m.item_name, m.item_price, c.item_quantity, c.item_total'
        '    FROM menu m'
        '    INNER JOIN cart c'
        '    ON m.id = c.item_menu_id'
        '    WHERE c.customer_id = ?',
        (customer_id,)
    ).fetchall()

    if bag is not None:
        for item in bag:
            new_price = modify_price(item['item_price'])
            item['item_price'] = new_price

    return bag


def delete_item(id: int, customer_id: int):
    """ In real application you should have customer id """
    db = database.get_db()
    db.execute(
        'DELETE FROM cart'
        '   WHERE item_menu_id = ?'
        '   AND customer_id = ?',
        (id, customer_id)
    )

    db.commit()

def delete_cart(customer_id: int):
    """ In real application you have customer id """
    db = database.get_db()
    db.execute(
        'DELETE FROM cart'
        '   WHERE customer_id = ?',
        (customer_id,)
    )

    db.commit()
