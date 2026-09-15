def show_dish(name, price, category):  #  Показывает информацию о блюде
    return f"{name} ({category}) — {price} руб."


def check_availability(in_stock):  #  Показывает в наличии ли блюдо
    if in_stock:
        return "Блюдо в наличии"
    return "Блюдо временно недоступно"


def calculate_order(price, quantity, discount_percent):  #  Считает итоговую стоимость заказа с учётом скидки.
    total = price * quantity
    discount = total * discount_percent / 100
    return total - discount


dish_name = "Капучино"
dish_price = 250.0
dish_category = "Напитки"
dish_in_stock = True

order_quantity = 2
order_discount = 10.0

print("=== Электронное меню ===")
print(show_dish(dish_name, dish_price, dish_category))
print(check_availability(dish_in_stock))

order_total = calculate_order(dish_price, order_quantity, order_discount)
print(f"Заказ: {order_quantity} x {dish_name}")
print(f"Скидка: {order_discount}%")
print(f"Итого к оплате: {order_total:.2f} руб.")
