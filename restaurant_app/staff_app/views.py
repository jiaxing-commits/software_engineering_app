from django.shortcuts import render, redirect
from db_models.models import Current_Orders, Customer, Order_history, Staff

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
        for i in total_orders: 
            if i.customer_id != -1:
                customer = Customer.objects.get(customer_id = i.customer_id) 
                request_status.append(customer.customer_request_status)
            else:
                request_status.append("In Progress")
        total_orders = [[x,y] for (x,y) in zip(total_orders, request_status)]
        context = { 'total_orders': total_orders }


        return render(request, 'staff_app/employee_portal.html', context)
    else:
        return redirect('login')