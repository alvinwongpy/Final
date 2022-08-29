from genericpath import exists
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth.models import User
from . models import CartOrder, CartOrderDetail
import datetime
from menu_items.models import Item

def cart(request):
    if request.user.is_authenticated:
        
        if request.method == 'POST':
            
            #check current user id
            current_user = request.user 
            userID = current_user.id
            itemID = request.POST['itemID']
            itemName = request.POST['itemName']
            orderQty = request.POST['orderQty']
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
                
                cart_order_details = CartOrderDetail.objects.filter(cartorder_id =cart_order.pk).values()
                
                print(cart_order_details)
                
                if cart_order_details.exists(): # cart_order_details exists
                    
                        if CartOrderDetail.objects.filter(item_id = itemID).exists():
                            # cart_order_details has reocrd with same item
                            cart_order_detail =  CartOrderDetail.objects.get(item_id = itemID)
                            q=int(orderQty)
                            cart_order_detail.qty = cart_order_detail.qty + q
                            cart_order_detail.save()
                        else:
                            # cart_order_details has no record with same item
                            cart_order_detail = CartOrderDetail(
                                cartorder_id = cart_order.pk,
                                item_id = itemID,
                                qty = orderQty,
                                price = itemPrice,
                                is_confirmed = False)
                            
                            cart_order_detail.save()
                        
                        cart_order_details = CartOrderDetail.objects.filter(cartorder_id =cart_order.pk).values()
                        print(cart_order_details)
                
                else: # cart_order_details not exist
                    
                    cart_order_detail = CartOrderDetail(
                        cart_order_id = cart_order.pk,
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
            
            for cart_order_detail in cart_order_details:
                item_id = cart_order_detail['item_id']
                temp = get_object_or_404(Item, pk=item_id)
                photo = temp.item_photo
                print(photo)
                cart_order_detail['photo'] = photo
                
                 
                #selected_item = items.objects.filter(pk=cart_order_detail.item_id)
                #photo = selected_item.item_photo 
                #setattr(cart_order_detail, 'photo', photo)
            
            context = {
                
                "cart_order_details" : cart_order_details, 
            
            }
            
            print(context)
            
            return render(request, 'accounts/shopping_test.html', context)
        
        else: 
            return redirect('accounts/shopping_cart.html')
    else:
        #return render(request,'pages/menu.html')
        return redirect('accounts/shopping_cart.html')

def test(request):
    return redirect('index')
