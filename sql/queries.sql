-- 1. Список всех блюд с названием категории (SELECT + JOIN)
SELECT d.id, d.name, c.name AS category, d.price, d.in_stock
FROM dishes AS d JOIN categories AS c ON c.id = d.category_id
ORDER BY d.name;

-- 2. Список всех категорий меню
SELECT id, name FROM categories ORDER BY name;

-- 3. Список пользователей
SELECT id, name, email FROM users ORDER BY name;

-- 4. Поиск блюд по категории (WHERE, параметр: category_id)
SELECT id, name, price FROM dishes WHERE category_id = ? ORDER BY name;

-- 5. Блюда не дороже указанной цены (WHERE, параметр: max_price)
SELECT id, name, price FROM dishes WHERE price <= ? ORDER BY price;

-- 6. Только доступные блюда
SELECT id, name, price FROM dishes WHERE in_stock = 1 ORDER BY price;

-- 7. Заказы с данными блюда и пользователя (JOIN)
SELECT o.id, d.name AS dish_name, u.name AS user_name, o.quantity,
       o.discount_percent, o.is_cancelled,
       ROUND(d.price * o.quantity * (1 - o.discount_percent / 100.0), 2) AS total
FROM orders AS o
JOIN dishes AS d ON d.id = o.dish_id
JOIN users AS u ON u.id = o.user_id
ORDER BY o.id;

-- 8. Активные заказы с данными блюда
SELECT o.id, d.name AS dish_name, u.name AS user_name, o.quantity
FROM orders AS o
JOIN dishes AS d ON d.id = o.dish_id
JOIN users AS u ON u.id = o.user_id
WHERE o.is_cancelled = 0
ORDER BY o.id;

-- 9. Количество блюд в меню
SELECT COUNT(*) AS dishes_count FROM dishes;

-- 10. Минимальная, максимальная и средняя цена блюд
SELECT MIN(price) AS min_price, MAX(price) AS max_price,
       ROUND(AVG(price), 2) AS average_price
FROM dishes;

-- 11. Количество блюд в каждой категории (GROUP BY)
SELECT c.name AS category, COUNT(d.id) AS dishes_count
FROM categories AS c
LEFT JOIN dishes AS d ON d.category_id = c.id
GROUP BY c.id, c.name
ORDER BY c.name;

-- 12. Сумма активных заказов по каждому пользователю (GROUP BY + HAVING)
SELECT u.name AS user_name,
       ROUND(SUM(d.price * o.quantity * (1 - o.discount_percent / 100.0)), 2) AS total_sum,
       COUNT(o.id) AS orders_count
FROM orders AS o
JOIN users AS u ON u.id = o.user_id
JOIN dishes AS d ON d.id = o.dish_id
WHERE o.is_cancelled = 0
GROUP BY u.id, u.name
HAVING COUNT(o.id) >= ?
ORDER BY total_sum DESC;
