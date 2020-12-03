from django.shortcuts import render, redirect
from db_models.models import Current_Orders, Customer, Order_history, Staff
import json

# Create your views here.

user = ''

def employee_portal(request):
    if 'Logged_Status' in request.session.keys() and request.session['Logged_Status'] == 'LOGGED':
        if 'User' in request.session:
            user = request.session['User']
        if request.method == 'POST':
            id = ""
            which = ""
            if request.POST.get('delete'):
                id = request.POST.get('delete')
                which = "Deleted"
            elif request.POST.get('fulfil'):
                id = request.POST.get('fulfil')
                which = "Fulfilled"
            current_order = Current_Orders.objects.get(order_id = id)
            piece_of_history = Order_history(order_id = current_order.order_id, customer_id = current_order.customer_id, item_list = current_order.item_list, total_price = current_order.total_price, order_status = which, staff_id = Staff.objects.get(email = user).staff_id)
            piece_of_history.save()
            current_order.delete()      
                
        total_orders = Current_Orders.objects.all()
        request_status = []
        all_prep_time = []
        for i in total_orders: 
            y = json.loads(i.item_list)
            add_price = len(y) * 2
            prep_time = 30 + add_price
            all_prep_time.append(prep_time)
            if i.customer_id != -1:
                customer = Customer.objects.get(customer_id = i.customer_id) 
                request_status.append(customer.customer_request_status)
            else:
                request_status.append("In Progress")
        total_orders = [[x,y,z] for (x,y,z) in zip(total_orders, request_status, all_prep_time)]
        context = { 'total_orders': total_orders}

    # total_items = 0

    # for x, y in cart.items():
    #     total_items += y[1]

        return render(request, 'staff_app/employee_portal.html', context)
    else:
        return redirect('login')