#from asyncio import queues
#from asyncio.windows_events import NULL
from genericpath import exists
from pickle import TRUE
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth.models import User 
from . models import CartOrder, CartOrderDetail
import datetime
from menu_items.models import Item
from decimal import Decimal

# import for PDF generation
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
# from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

# from django.http import HttpResponse
from django.template.loader import render_to_string
# from django.template import RequestContext
# from django.conf import settings
# from xhtml2pdf import pisa
# import io as StringIO
# from io import BytesIO
# import cgi
# import os


def cart(request):
    if request.user.is_authenticated: # check if user has login
        
        # user has login and check if user has POST data
        if request.method == 'POST':
                        
            # check OrderQty if it is figure
            def isNum(data):
                try:
                    int(data)
                    return True
                except ValueError:
                    return False
                
            orderQty = request.POST['orderQty']
            if isNum(orderQty) == False:
                messages.error(request, "Please input valid figure. Thank you")
                # example : messages.error(request, 'Email box full', extra_tags='email')
                return redirect('menu') #if input is figure then return to menu  
            
            if int(orderQty) == 0 or int(orderQty) < 0 :
                messages.error(request, "Please input vaild figure. Thank you")
                # example : messages.error(request, 'Email box full', extra_tags='email')
                return redirect('menu') #if input is figure then return to menu
            
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
            # total_include_tax
            total_include_tax = total + tax_amount
            tax_amount = "{:.2f}".format(tax_amount)
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
                    first_name = current_user.first_name
                    last_name = current_user.last_name
                                    
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
                        "first_name"   : first_name,
                        "last_name"    : last_name,
                        
                    }
                    # user has login and POST has data and has CartOrder 
                    return render(request, 'accounts/shopping_cart.html', context) 
                    #return render(request, 'accounts/shopping_cart.html', context)         
            
            else: # user has login but not POST data and check user has no CartOrder          
                return render(request, 'accounts/shopping_cart.html')
    
    else: # user has no login
        return render(request,'login')


def cart_test(request):
    return

def cart_pdf(request):
    
    if request.method == 'POST':
        
        UserPhone = request.POST['phone']
        
        if UserPhone :
        
                current_user = request.user
                userID = current_user.id
                # user has login but not POST data and user has cart order 
                cart_order = CartOrder.objects.get(user_id = userID)
                            
                print(cart_order.pk)
                
                cart_order_details = CartOrderDetail.objects.filter(cartorder_id =cart_order.pk)
                
                index=[]
                for cart_order_detail in cart_order_details:
                    index.append(cart_order_detail.pk)
                    
                inv_number = 1000*cart_order.pk + max(index)
                            
                cart_order_details = CartOrderDetail.objects.filter(cartorder_id =cart_order.pk).values()
                            
                print(cart_order_details)
                                            
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
                first_name = current_user.first_name
                last_name = current_user.last_name
                                
                current_date = datetime.date.today() 
                
                print(cart_order_details)
                                
                context = {
                                    "cart_order_details" : cart_order_details, 
                                    "qty_sum" : qty_sum,
                                    "tax_amount" : tax_amount,
                                    "total_include_tax" : total_include_tax,
                                    "total" : total,
                                    "username" : username,
                                    "email" : email,
                                    "current_date" : current_date,
                                    "inv_number"   : inv_number,
                                    "first_name"   : first_name,
                                    "last_name"    : last_name,
                                    "phone"        : UserPhone,
                                   
                }
                messages.success(request, "Please pay this invoice. Thank you")
                return render(request, 'accounts/test_pdf.html', context)
        
        else: # POST with confirm order but no phone number input
            
            return redirect('cart')

    else: # No POST data
        return redirect('index')




    # path = "accounts/test_note.html"
   
    # html = render_to_string('accounts/test_note.html',context)
    # io_bytes = BytesIO()
    
    # pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), io_bytes)
    
    # if not pdf.err:
    #     return HttpResponse(io_bytes.getvalue(), content_type='application/pdf')
    # else:
    #     return HttpResponse("Error while rendering PDF", status=400)



    
#     template_path = 'accounts/test_note.html'
#     #context = {'myvar': 'this is your template context'}
#     # Create a Django response object, and specify content_type as pdf
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="report.pdf"'
#     # find the template and render it.
#     template = get_template(template_path)
#     html = template.render(context)

#     # create a pdf
#     pisa_status = pisa.CreatePDF(
#        html, dest=response, link_callback=link_callback)
#     # if error then show some funny view
#     if pisa_status.err:
#        return HttpResponse('We had some errors <pre>' + html + '</pre>')
#     return response



    
# def link_callback(uri, rel):

#     sUrl = settings.STATIC_URL
#     sRoot = settings.STATIC_ROOT
#     mUrl = settings.MEDIA_URL
#     mRoot = settings.MEDIA_ROOT

#     if uri.startswith(mUrl):
#         path = os.path.join(mRoot, uri.replace(mUrl, ""))
#     elif uri.startswith(sUrl):
#         path = os.path.join(sRoot, uri.replace(sUrl, ""))
#     else:
#         return uri

#     if not os.path.isfile(path):    
#         raise Exception( 'media URI must start with %s or %s' % (sUrl, mUrl))

#     return path
    
    
    
#     html  = render_to_string('accounts/shopping_cart.html', { 'pagesize' : 'A4', }, context)
#     result = StringIO.StringIO()
#     pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), dest=result, link_callback=fetch_resources )
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), mimetype='application/pdf')
#     return HttpResponse('Gremlins ate your pdf! %s' % cgi.escape(html))

# def fetch_resources(uri, rel):
#     path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))

#     return path
    
    
                    
#    html = render_to_string('accounts/shopping_cart.html',context)
#    io_bytes = BytesIO()
#    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), io_bytes, link_callback=fetch_resources)
                    
#    if not pdf.err:
#        return HttpResponse(io_bytes.getvalue(), content_type='application/pdf')
#    else:
#        return HttpResponse("Error while rendering PDF", status=400)
