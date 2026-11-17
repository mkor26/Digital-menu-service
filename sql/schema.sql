-- Схема базы данных Digital Menu Service
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS dishes (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    price REAL NOT NULL CHECK (price >= 0),
    in_stock INTEGER NOT NULL DEFAULT 1 CHECK (in_stock IN (0, 1)),
    description TEXT NOT NULL DEFAULT '',
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    dish_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1 CHECK (quantity > 0),
    discount_percent REAL NOT NULL DEFAULT 0 CHECK (discount_percent BETWEEN 0 AND 100),
    is_cancelled INTEGER NOT NULL DEFAULT 0 CHECK (is_cancelled IN (0, 1)),
    FOREIGN KEY (dish_id) REFERENCES dishes(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX IF NOT EXISTS idx_dishes_category_id ON dishes(category_id);
CREATE INDEX IF NOT EXISTS idx_orders_dish_id ON orders(dish_id);
CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders(user_id);
