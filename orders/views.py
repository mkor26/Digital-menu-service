from django.shortcuts import render
from models.orders import find_order_by_id
from storage import load_all

def orders(request):
    _, _, orders_list = load_all()
    return render(request, "orders/order_list.html", {"orders": orders_list})

def order_detail(request, order_id):
    _, _, orders_list = load_all()
    order = find_order_by_id(orders_list, order_id)
    
    return render(
        request, 
        "orders/order_detail.html", 
        {"order": order},
        status=404 if order is None else 200
    )