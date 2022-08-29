from asyncio import queues
from genericpath import exists
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth.models import User 
from . models import CartOrder, CartOrderDetail
import datetime
from menu_items.models import Item
from decimal import Decimal

def cart(request):
    if request.user.is_authenticated: # check if user has login
        
        # user has login
        if request.method == 'POST':
            
            # user has login with POST data
            # check current user id
            current_user = request.user 
            userID = current_user.id
            itemID = request.POST['itemID']
            itemName = request.POST['itemName']
            orderQty = int(request.POST['orderQty'])
            itemPrice = request.POST['itemPrice']
            
            
            test={
                
                    "userID" : userID,
                    "itemID" : itemID,
                    "itemName" : itemName,
                    "orderQty" : orderQty,
                    "itemPrice" : itemPrice,
                
            }
                
            print(test)
            
            # auth_user has one and only one CartOder 
            # and no more than one CartOder forever 
            # even login again to be deal with the same one CartOder
            # it is wanted  that CartOder is designed as a notes record 
            # for user to select items for management of user's ordering 
            
            if CartOrder.objects.filter(user_id = userID).exists():
                
                # cart order exist
                cart_order = CartOrder.objects.get(user_id = userID)
                
                print(cart_order.pk)
                
                if CartOrderDetail.objects.filter(cartorder_id =cart_order.pk, item_id=itemID).exists():
                    
                    cart_order_detail = CartOrderDetail.objects.get(cartorder_id =cart_order.pk, item_id=itemID)
                    cart_order_detail.qty = cart_order_detail.qty + orderQty
                    cart_order_detail.save()
    
                    cart_order_details = CartOrderDetail.objects.filter(cartorder_id =cart_order.pk).values()
                    print(cart_order_details)
                
                else: # cart_order_details not exist
                    
                    cart_order_detail = CartOrderDetail(
                        cartorder_id = cart_order.pk,
                        item_id = itemID,
                        qty = orderQty,
                        price = itemPrice,
                        is_confirmed = False)
                    
                    cart_order_detail.save()
                    
                    cart_order_details = CartOrderDetail.objects.filter(cartorder_id =cart_order.pk).values()
                
 
                
            else:  # cart order not exist
                   
                cart_order=CartOrder(user_id=userID, selection_date=datetime.date.today())
                
                cart_order.save()
                
                cart_order = CartOrder.objects.get(user_id = userID)
                
                cart_order_detail = CartOrderDetail(
                    cartorder_id = cart_order.pk, 
                    item_id=itemID, 
                    qty = orderQty, 
                    price = itemPrice , 
                    is_confirmed = False)
                
                cart_order_detail.save()
                
                cart_order_details = CartOrderDetail.objects.filter(cartorder_id =cart_order.pk).values()
                
            
            items = Item.objects.filter(is_displayed=True).values()
            
            print(items)
            
            #for item in items:
            #    lowercase = item.type.type_name
            #    lowercase = lowercase.lower()
            #    setattr(item, 'lowercase', lowercase)
            qty_sum=0
            for cart_order_detail in cart_order_details:
                item_id = cart_order_detail['item_id']
                qty_sum = qty_sum + cart_order_detail['qty']
                temp = get_object_or_404(Item, pk=item_id)
                photo = temp.item_photo
                name  = temp.item_name
                desc  = temp.item_desciption
                cart_order_detail['photo'] = photo
                cart_order_detail['name'] = name
                cart_order_detail['desc'] = desc
                price = cart_order_detail['price']
                qty = cart_order_detail['qty']
                sub_total = qty*price
                cart_order_detail['sub_total'] = sub_total
            
            # total $ for the whole cart order 
            total=0    
            for cart_order_detail in cart_order_details:
                 total = total + cart_order_detail['sub_total']
            
            # set tax rate
            tax_rate = 0.05
            # tax amount
            # Decimal(my_float)
            tax_amount = Decimal(tax_rate)*total
            tax_amount = "{:.2f}".format(tax_amount)
            # total_include_tax
            total_include_tax = total + tax_amount
            total_include_tax = "{:.2f}".format(total_include_tax)
                
                 
                #selected_item = items.objects.filter(pk=cart_order_detail.item_id)
                #photo = selected_item.item_photo 
                #setattr(cart_order_detail, 'photo', photo)
            
            current_user = request.user
            username = current_user.username
            email = current_user.email
            current_date = datetime.date.today() 
                
            context = {
                
                "cart_order_details" : cart_order_details, 
                "qty_sum" : qty_sum,
                "tax_amount" : tax_amount,
                "total_include_tax" : total_include_tax,
                "total" : total,
                "username" : username,
                "email" : email,
                "current_date" : current_date
            
            }
            
            print(context)
            
            return render(request, 'accounts/shopping_cart.html', context)
        
        else: # user has login but not POST data
            
            current_user = request.user
            userID = current_user.id
            
            # user has login but not POST data and check if user has CartOrder
            if CartOrder.objects.filter(user_id = userID).exists(): 
                
                # user has login but not POST data and user has cart order 
                cart_order = CartOrder.objects.get(user_id = userID)
                
                print(cart_order.pk)
                
                cart_order_details = CartOrderDetail.objects.filter(cartorder_id =cart_order.pk).values()
                
                print(cart_order_details)
                
                if cart_order_details.exists(): # cart_order_details exists
                    
                    items = Item.objects.filter(is_displayed=True).values()
                    
                    qty_sum=0
                    for cart_order_detail in cart_order_details:
                        item_id = cart_order_detail['item_id']
                        qty_sum = qty_sum + cart_order_detail['qty']
                        temp = get_object_or_404(Item, pk=item_id)
                        photo = temp.item_photo
                        name  = temp.item_name
                        desc  = temp.item_desciption
                        cart_order_detail['photo'] = photo
                        cart_order_detail['name'] = name
                        cart_order_detail['desc'] = desc
                        price = cart_order_detail['price']
                        qty = cart_order_detail['qty']
                        sub_total = qty*price
                        cart_order_detail['sub_total'] = sub_total 
                    
                    print(qty_sum)
                    
                     # total $ for the whole cart order 
                    total=0    
                    for cart_order_detail in cart_order_details:
                        total = total + cart_order_detail['sub_total']
            
                    # set tax rate
                    tax_rate = 0.05
                    # tax amount
                    tax_amount = Decimal(tax_rate)*total
                    # total_include_tax
                    total_include_tax = total + tax_amount
                    # float converting
                    tax_amount = "{:.2f}".format(tax_amount)
                    total_include_tax = "{:.2f}".format(total_include_tax) 
                    
                    current_user = request.user
                    username = current_user.username
                    email = current_user.email
                    
                    current_date = datetime.date.today() 
                    
                    context = {
                        "cart_order_details" : cart_order_details, 
                        "qty_sum" : qty_sum,
                        "tax_amount" : tax_amount,
                        "total_include_tax" : total_include_tax,
                        "total" : total,
                        "username" : username,
                        "email" : email,
                        "current_date" : current_date,
                        
                    }
                    return render(request, 'accounts/shopping_cart.html', context)         
            
            else: # user has login but not POST data and check user has no CartOrder          
                return render(request, 'accounts/shopping_cart.html')
    
    else: # user has no login
        return render(request,'login')

def test(request):
    return redirect('index')
