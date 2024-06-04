DROP TABLE IF EXISTS customers;
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

DROP TABLE IF EXISTS menu;
CREATE TABLE IF NOT EXISTS menu (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT NOT NULL,
    item_type TEXT NOT NULL,
    item_price REAL NOT NULL,
    item_picture_path TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS cart (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    item_menu_id INTEGER NOT NULL,
    item_quantity INTEGER NOT NULL,
    item_total REAL NOT NULL,
    is_random INTEGER NOT NULL, 
    FOREIGN KEY (item_menu_id) REFERENCES menu (id)
);

INSERT INTO menu
(item_name, item_type, item_price, item_picture_path)
VALUES
('Random Food Generator', 'DON', '20', 'static/images/question mark.jpg'),
('Chicken Teriyaki Don', 'DON', '10.90', 'static/images/Don/Chicken Teriyaki Don.jpg'),
('Gyu Don', 'DON', '10.70', 'static/images/Don/Gyu (Beef) Don.jpg'),
('Mini Salmon Avo Mentai Don', 'DON', '12.50', 'static/images/Don/Mini Salmon Avo Mentai Don.jpg'),
('Tempura Don', 'DON', '12.50', 'static/images/Don/Tempura Don.jpg'),
('Unagi Don', 'DON', '12.50', 'static/images/Don/Unagi Don.jpg'),
('Green Tea', 'DRINKS', '2.50', 'static/images/Drinks/Green Tea.jpg'),
('Coca Cola', 'DRINKS', '2.50', 'static/images/Drinks/Coca Cola.jpg'),
('Pepsi', 'DRINKS', '2.50', 'static/images/Drinks/Pepsi.jpg'),
('Plain Water', 'DRINKS', '2.50', 'static/images/Drinks/Plain Water.jpg'),
('Sprite', 'DRINKS', '2.50', 'static/images/Drinks/Sprite.jpg'),
('Hamachi Sashimi', 'SASHIMI', '20.50', 'static/images/Sashimi/Hamachi Sashimi (Yellowtail).jpg'),
('Maguro Sashimi', 'SASHIMI', '20.50', 'static/images/Sashimi/Maguro Sashimi (Tuna).jpg'),
('Premium Sashimi Platter', 'SASHIMI', '20.50', 'static/images/Sashimi/Premium Sashimi Platter.jpg'),
('Salmon Sashimi', 'SASHIMI', '20.50', 'static/images/Sashimi/Salmon Sashimi.jpg'),
('Sashimi Platter', 'SASHIMI', '20.50', 'static/images/Sashimi/Sashimi Platter.jpg');


INSERT INTO customers
(username, password)
VALUES
('john', 'p@55word'),
('adam', '123456'),
('samantha', '654321');
