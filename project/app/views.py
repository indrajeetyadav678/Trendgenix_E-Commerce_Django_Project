from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import*
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from .forms import*
from datetime import datetime
import razorpay
# from django.http import HttpResponse

# Create your views here.

# ================ registration function ================
def registerdata(request):
    print(request.method)
    name=request.POST.get('name')
    email=request.POST.get('email')
    print(email)
    number=request.POST.get('number')
    password=request.POST.get('password')
    con_password=request.POST.get('con_password')
    data=RegistrationModel.objects.filter(Email=email)
    if name=="" or email=="" or number=="" or password=="":
        msg="Please fill all data field"
        return render(request, 'register.html', {'key':msg,'data1':name,'data2':email,'data3':number})     
    else:
        if data:
            msg="User aleary Exist"
            Context={
                 'key':msg
            }
            return render(request, 'register.html', Context)
        else:
            if password==con_password:
                RegistrationModel.objects.create(
                    Name=name,
                    Email=email,
                    Number=number,
                    Password=password
                )
                
                subject = 'New Customer User Account'
                message = 'A New Customer register On Our Website'+name+'  '+number+'  '+email+'  '+password
                email_from = email
                recipient_list = ['indrajeetyadu36@gmail.com']
                send_mail(subject, message, email_from, recipient_list)
                msg="Registration Successfully Done"
                return render(request, 'login.html', {'key': msg})
            else:
                msg="Password and Confirm Password Not Match"
                Context={'key':msg,
                         'data1':name,
                         'data2':email,
                         'data3':number
                         }
                return render(request, 'register.html',Context )


# ============= login function =====================
   
def logindata(request):
    email=request.POST.get('email')
    password=request.POST.get('password')
    login_type=request.POST.get('login_type')
    # print(login_type)
    username=RegistrationModel.objects.filter(Email=email)
    if login_type=='none':
        msg="Choose your login Type"
        return render(request, 'login.html', {'key1': msg})
    elif login_type =='customer':
        if username:
            data=RegistrationModel.objects.get(Email=email)
            print(data)
            print("*********************************************")
            
            Password= data.Password
            print(Password)
            if Password==password:
                msg="Welcome To "+data.Name
                request.session['user_info'] = {
                    # 'Profile':data.Profile,
                    'Username':data.Username,
                    'About':data.About,
                    'Name':data.Name,
                    'Email':data.Email,
                    'Number':data.Number,
                    'Password':data.Password,
                    'Login_Type': login_type 
                }
                user_info=request.session.get('user_info')
                print('user_info-->',user_info)
                Context={
                         'key1': msg, 
                         'user_name':user_info, 
                         'media_url':settings.MEDIA_URL
                        }
                return render(request, 'index.html',Context )
            else:
                msg="Enter Password is Wrong Please Enter Correct Password"
                return render(request, 'login.html', {'key1': msg})
        else:
            msg="Userid doesnot exist Please create Account"
            return render(request, 'register.html', {'key1': msg})
    elif login_type =="admin":
        if username:
            data=RegistrationModel.objects.get(Email=email)
            print(data.Name)
            print(data)
            Password= data.Password
            if Password==password:
                Context={}

                # Context['Profile']=request.session['Profile']= data.Profile
                Context['Username']=request.session['Username']= data.Username
                Context['About']=request.session['About']= data.About
                Context['Name']=request.session['Name']= data.Name
                Context['Email']=request.session['Email']= data.Email
                Context['Number']=request.session['Number']= data.Number
                Context['Password']=request.session['Password']= data.Password
                # Context['Name']=request.session['id']= data.id
                print(data.Name)
                msg="Welcome To "+data.Name
                return render(request, 'dashboard.html', {'key1': msg, 'admin_user':data})
            else:
                msg="Enter Password is Wrong Please Enter Correct Password"
                return render(request, 'login.html', {'key1': msg})
        else:
            msg="Userid doesnot exist Please create Account"
            return render(request, 'register.html', {'key1': msg})
        
# ============================== logout ===================================
def logout(request):
    return render(request, 'index.html')


def forgetpass(request):
    return render(request, 'forgetpass.html')

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@---- User Dashboard -----@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#====================== Starting user Dashboard (Navigation) =======================

def index(request):
    try:
        user_info=request.session.get('user_info')
        return render(request, 'index.html', {'user_name':user_info})
    except:
        return render(request, 'index.html')

def about(request):
    try:
        user_info=request.session.get('user_info')           
        return render(request, 'about.html', {'user_name':user_info})
    except:
        return render(request, 'about.html')

def contact(request):
    try:
        user_info=request.session.get('user_info')
        return render(request, 'contact.html', {'user_name':user_info})
    except:
        return render(request, 'contact.html')

def register(request):
    return render(request, 'register.html')

def login(request):
    return render(request, 'login.html')

def product(request):
    try:
        user_info=request.session.get('user_info')
        return render(request, 'product.html', {'user_name':user_info})
    except:
        return render(request, 'product.html')

# ----------------- starting Product page navigation -------------------------
def men(request):
    data=Productmodel.objects.filter(Prod_Name="Men")
    print(data.values()) 
    try:
        user_info=request.session.get('user_info')
        Context={
            'prop':data,
            'media_url': settings.MEDIA_URL,
            'user_name':user_info
        }
        return render(request, 'men.html',Context)
    except:
        Context={
            'prop':data,
            'media_url': settings.MEDIA_URL
        }
        return render(request,'men.html',Context )


def women(request):
    data=Productmodel.objects.filter(Prod_Name="Men")
    print(data.values())
    try:
        user_info=request.session.get('user_info')
        Context={
        'prop':data,
        'media_url': settings.MEDIA_URL,
        'user_name':user_info
    }
        return render(request, 'women.html', Context)
    except:
        Context={
        'prop':data,
        'media_url': settings.MEDIA_URL
    }
        return render(request, 'women.html',Context)

def girl(request):
    data=Productmodel.objects.filter(Prod_Name="Girl")
    # print(data.values())
    try:
        user_info=request.session.get('user_info')
        Context={
        'prop':data,
        'media_url': settings.MEDIA_URL,
        'user_name':user_info
    }
        return render(request, 'girl.html', Context )
    except:
        Context={
            'prop':data,
            'media_url': settings.MEDIA_URL
        }
        return render(request, 'girl.html', Context)
    
# ====================== Starting User Dashboard (Add to Cart) =============================================
#  =---------------------- Starting Cart add Button -----------------------------------------------
def addtocart(request, pk):
    # user_info=request.session.get('user_info')
    email = request.POST.get('email')
    prod_name = request.POST.get('prod_name')
    if email:
        data = RegistrationModel.objects.get(Email=email)
        addtocart = request.session.get('addtocart', [])
        if pk not in [item['id'] for item in addtocart]:
            add_cartdata = {
                'id': pk,
                'Quantity': 1
            }
            addtocart.append(add_cartdata)
        request.session['addtocart'] = addtocart
        addedcartno = len(addtocart)
        user_info=data
        if prod_name == 'Men':
            prod_data1 = Productmodel.objects.filter(Prod_Name='Men')
            return render(request, 'men.html', {'user_name': user_info, 'prop': prod_data1, 'addcartno': addedcartno, 'media_url': settings.MEDIA_URL})
        elif prod_name == 'Women':
            prod_data1 = Productmodel.objects.filter(Prod_Name='Women')
            return render(request, 'women.html', {'user_name': user_info, 'prop': prod_data1, 'addcartno': addedcartno, 'media_url': settings.MEDIA_URL})
        elif prod_name == 'Kids':
            prod_data1 = Productmodel.objects.filter(Prod_Name='Kids')
            return render(request, 'girl.html', {'user_name': user_info, 'prop': prod_data1, 'addcartno': addedcartno, 'media_url': settings.MEDIA_URL})
    else:
        return redirect('login')
    
#  =---------------------- ENDing Cart add Button -----------------------------------------------

def cartpage(request):
    # email = request.POST.get('email')
    # data = RegistrationModel.objects.get(Email=email)
    user_info=request.session.get('user_info')
    try:
        addcart_data = request.session.get('addtocart', [])
        # print(addcartround(_data)
        total_MRP = 0
        total_amount = 0
        tax = 0
        shippingcharge = 40
        Quantity=0
        pro_data = []
        for item in addcart_data:
            # print(item)
            pro_value = Productmodel.objects.get(id=item['id'])
            # print(pro_value)
            pro_quantitydata = {
                'pro_value': pro_value,
                'Quantity': item['Quantity']
            }
            pro_data.append(pro_quantitydata)
            # print(pro_quantitydata)
            total_amount += pro_value.Prod_Price * item['Quantity']
            total_MRP += pro_value.Prod_MRP * item['Quantity']
            tax += int(round((total_amount * 12) / 100,0))
            Quantity += item['Quantity']

        discount = total_MRP - total_amount
        Total_pay_amount = total_amount + shippingcharge + tax

        billamount = {
            'total_amount': total_amount,
            'total_MRP': total_MRP,
            'discount': discount,
            'tax': tax,
            'shippingcharge': shippingcharge,
            'Total_pay_amount': Total_pay_amount,
            'Quantity':Quantity     
        }
        Context={
            'user_name': user_info, 
            'prod_data': pro_data, 
            'media_url': settings.MEDIA_URL, 
            'amount': billamount
        }
        return render(request, 'addtocart.html', Context)
    except:
        return render(request, 'login.html')


# ====================== Ending User Dashboard (Add to Cart) =============================================
 
# ======================== Starting user profile Function ==========================================

def editpro(request):
    
    try:
        data={}
        data['Name']=request.session.get('Name')
        data['Email']=request.session.get('Email')
        data['Number']=request.session.get('Number')
        data['Password']=request.session.get('Password')
        # print(data)
        Context={
            'admin_user':data,
        }
        return render(request, 'editprofile.html', Context)
    except:
        user_info=request.session.get('user_info')
        Context={
            'user_name': user_info,
        }
        return render(request, 'editprofile.html', Context)



def changepass(request):
    try:
        data={}
        data['Name']=request.session['Name']
        data['Email']=request.session['Email']
        data['Number']=request.session['Number']
        data['Password']=request.session['Password']
        return render(request, 'changepass.html', {'admin_user':data})
    except:
        user_info=request.session.get('user_info')
        return render(request, 'changepass.html', {'user_name':user_info})


def passwordchange(request):
    if request.method=='POST':
        email=request.POST.get('email')
        print(email)
        login_type=request.POST.get('login_type')
        newpassword=request.POST.get('newpassword')
        conpassword=request.POST.get('conpassword')
        register = get_object_or_404(RegistrationModel, Email=email)
    try:
        if newpassword == conpassword:
            print(register)
            register.Password = newpassword
            register.save(update_fields=['Password'])

            msg="Password successfully Changed"
            data1 = get_object_or_404(RegistrationModel, Email=email)
            request.session['user_info']={
                # 'Profile':data1.Profile,
                'Name':data1.Name,
                'Email':data1.Email,
                'Number':data1.Number,
                'Password':data1.Password,
                'Login_Type': login_type    
            }
            user_info=request.session.get('user_info')
            Context={
                'key':msg,
                'user_name':user_info
            }    
            return render(request, 'index.html',Context)
    except:

        if newpassword == conpassword:
            register.Password = newpassword
            register.save(update_fields=['Password'])
            request.session['Password']=newpassword
            msg="Password successfully Changed"
        data1 = get_object_or_404(RegistrationModel, Email=email)
        data={}
        data['Name']=request.session['Name']=data1.Name
        data['Email']=request.session['Email']=data1.Email
        data['Number']=request.session['Number']=data1.Number
        data['Password']=request.session['Password']=data1.Password
        Context={
            'key':msg,
            'admin_user':data
        }
        return render(request, 'dashboard.html', Context)    

    
#========================= Endinging user profile Function ==========================================
#========================= ENDing user Dashboard (Navigation) ========================================

# ============ Show Product Data ================
def showmenproductdata(request):
    data=Productmodel.objects.filter(Prod_Name="women")
    # print(data.values())
    return render(request,'men.html',{'prop':data,'media_url': settings.MEDIA_URL} )



# =================== Startinging User Dashboard (Razorpay payment integrations) ================================

def checkout(request):
    amount=int(request.POST.get('amount'))*100
    # print(amount)
    email=request.POST.get('email')
    # print(email)
    userdata=RegistrationModel.objects.get(Email=email)
    global Payableamount 
    # amount in paisa
    client = razorpay.Client(auth =("rzp_test_8jTLUV3aVex82Q" , "n3PL7ZbSgnKSWJeA1s9ndhaO"))
    # amount = int(amount * 100)
    #create order
    data = { "amount": amount, "currency": "INR", "receipt": "order_rcptid_11" }
    # print(data)
    payment = client.order.create(data=data)
    print("Payment ----->",payment)
    Payableamount=payment

    print(payment['id'])
    PaymentdataModel.objects.create(
        Email=email,
        Amount=payment['amount'],
        Amount_paid=payment['amount_paid'],
        Amount_due=payment['amount_due'],
        Currency=payment['currency'],
        Receipt =payment['receipt'],
        Status=payment['status'],
        Attempts=payment['attempts'],
        Notes=payment['notes'],
        Created_at=payment['created_at'], 
        Order_id=payment['id']
    )
    addcart_data = request.session.get('addtocart', [])
    # print(addcartround(_data)
    total_MRP = 0
    total_amount = 0
    tax = 0
    shippingcharge = 40
    Quantity=0
    pro_data = []

    for item in addcart_data:
        # print(item)
        pro_value = Productmodel.objects.get(id=item['id'])
        # print(pro_value)
        pro_quantitydata = {
            'pro_value': pro_value,
            'Quantity': item['Quantity']
        }
        pro_data.append(pro_quantitydata)
        # print(pro_quantitydata)
        total_amount += pro_value.Prod_Price * item['Quantity']
        total_MRP += pro_value.Prod_MRP * item['Quantity']
        tax += int(round((total_amount * 12) / 100,2))
        Quantity += item['Quantity']

    discount = total_MRP - total_amount
    Total_pay_amount = total_amount + shippingcharge + tax
    
    billamount = {
        'total_amount': total_amount,
        'total_MRP': total_MRP,
        'discount': discount,
        'tax': tax,
        'shippingcharge': shippingcharge,
        'Total_pay_amount': Total_pay_amount,
        'Quantity':Quantity
    }

    cart_length = len(addcart_data)
    user_info=request.session.get('user_info')
    Context={
        'user_name': user_info, 
        'pay_data':data, 
        'media_url': settings.MEDIA_URL,
        'payment':payment,
        'amount': billamount,
        'prod_data': pro_data,
        'length':cart_length
    }
    # print(payment)
    return render(request, 'addtocart.html', Context)
#  -------------------- MakePayment -----------------------------------
@csrf_exempt
def making_payment(request):
    print('******************')
    # print(request.POST)
    razorpay_payment_id = request.POST.get('razorpay_payment_id')
    razorpay_order_id = request.POST.get('razorpay_order_id')
    email = request.POST.get('email')
    print(razorpay_order_id)
    razorpay_signature = request.POST.get('razorpay_signature')
    payment_data= get_object_or_404(PaymentdataModel, Order_id=razorpay_order_id)
    print(payment_data)
    payment_data.Payment_Id = razorpay_payment_id
    payment_data.Signature = razorpay_signature
    
    user_info=request.session.get('user_info')
    # Save the updated payment data
    payment_data.save(update_fields=['Payment_Id', 'Signature'])
    if 'addtocart' in request.session:
        del request.session['addtocart']
    print(user_info)
    Context={
         'user_name': user_info,
    }
    return render(request, 'paymentdone.html', Context)

# ====================== Ending User Dashboard (Razorpay payment integrations) ======================================



# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  Admin Dashboard Views Function @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    #===================Starting Admin dashboard (Navigation)============================

def dashbordindex(request):
    data={}
    data['Name']=request.session['Name']
    data['Email']=request.session['Email']
    data['Number']=request.session['Number']
    data['Password']=request.session['Password']
    return render(request, 'dashboardindex.html', {'admin_user':data}) 

def productdata(request):
    data={}
    data['Name']=request.session['Name']
    data['Email']=request.session['Email']
    data['Number']=request.session['Number']
    data['Password']=request.session['Password']
    Context={
        'admin_user':data,
        'f_content':Context,
        'prod_form':Productmodelform
    }
    
    return render(request, 'productdata.html',Context )

def userdata(request):
    data={}
    data['Name']=request.session['Name']
    data['Email']=request.session['Email']
    data['Number']=request.session['Number']
    data['Password']=request.session['Password']
    return render(request, 'userdata.html', {'admin_user':data})

def result(request):
    data={}
    data['Name']=request.session['Name']
    data['Email']=request.session['Email']
    data['Number']=request.session['Number']
    data['Password']=request.session['Password']
    return render(request, 'result.html', {'admin_user':data})

def product_entry(request):
    data={}
    data['Name']=request.session['Name']
    data['Email']=request.session['Email']
    data['Number']=request.session['Number']
    data['Password']=request.session['Password']
    if request.method == "POST":
        # print(request.POST)
        # print(request.FILES)
        serialno=request.POST.get('Serial_no')
        serialmodel=Productmodel.objects.filter(Serial_no=serialno)
        if serialmodel:
            msg = "This data already exist "
            return render(request, 'productform.html', {'msg': msg, 'admin_user':data})
        else:
            form = Productmodelform(request.POST, request.FILES)
        # print(form)
            if form.is_valid():
                form.save()
                msg = "Data submitted successfully"
                return redirect('productdata')
            else:
                msg = "There is some error, please try again"
                return render(request, 'productform.html', {'msg': msg, 'admin_user':data})
    else:
        form = Productmodelform()
        return render(request, 'productform.html', {'admin_user':data})
    
#======================= ENDing Admin dashboard (Navigation) =================================
    
# ====================== Starting admin Dashboard (Todo task CRUD) ============================  
def  todoform(request):
    data={}
    data['Name']=request.session['Name']
    data['Email']=request.session['Email']
    data['Number']=request.session['Number']
    data['Password']=request.session['Password']
    msg="open task form"
    return render(request, 'dashboard.html',{'admin_user':data, 'show':msg} )

def todotask(request):
    # print(request.POST)
    title = request.POST.get('title')
    task = request.POST.get('task')
    email = request.POST.get('email')
    # password = request.POST.get('password')
    data={}
    data['Name']=request.session['Name']
    data['Email']=request.session['Email']
    data['Number']=request.session['Number']
    data['Password']=request.session['Password']
    data=RegistrationModel.objects.get(Email=email)
    taskcheck=Todolist.objects.filter(Title=title)
    if taskcheck:
        msg="This Tutle task Already Saved"  
        return render(request, 'dashboard.html', {'key1': msg, 'admin_user':data})   
    else:
        Todolist.objects.create(
            Title=title,
            Task=task,
            Email=email
        )
        msg="Your Task is Saved"
        return render(request, 'dashboard.html', {'key1': msg, 'admin_user':data})


# def search(request):
#     date=request.POST.get('date')
#     print(date)
#     email=request.POST.get('email')
#     print(email)
#     data=RegistrationModel.objects.get(Email=email)
#     taskdata=Todolist.objects.filter(Date=date) and Todolist.objects.filter(Email=email) 
#     # if taskdata:
#     #     return render(request, 'dashboard.html', {'user_name':data, 'tododata':taskdata})
#     # else:
#     #     msg="data not found"
#     #     return render(request, 'dashboard.html', { 'key1':msg, 'user_name':data})
#     return render(request, 'dashboard.html')


def showdata1(request, pk):
    # print(pk)
    # data=RegistrationModel.objects.filter(Email=pk)
    data={}
    data['Name']=request.session['Name']
    data['Email']=request.session['Email']
    data['Number']=request.session['Number']
    data['Password']=request.session['Password']
    taskdata=Todolist.objects.filter(Email=data['Email'])
    return render(request, 'dashboard.html', {'admin_user':data, 'tododate':taskdata})

def showdata2(request):
    email=request.POST.get('email')
    # print(email)
    data=RegistrationModel.objects.get(Email=email)
    # print(data)
    taskdata=Todolist.objects.filter(Email=email)
    # print(taskdata)
    # print(taskdata.values())
    return render(request, 'dashboard.html', {'admin_user':data, 'tododate':taskdata})


def edittodo(request, pk):
    # print(pk)
    data1=Todolist.objects.get(id=pk)
    email=data1.Email
    taskdata=Todolist.objects.filter(Email=email)
    data=RegistrationModel.objects.get(Email=email)
    return render(request, 'dashboard.html', {'admin_user':data, 'tododate':taskdata, 'taskobject':data1})

def delettodo(request, pk):
    # print(pk)
    data=Todolist.objects.get(id=pk)
    email=data.Email
    data.delete()
    taskdata=Todolist.objects.filter(Email=email)
    data=RegistrationModel.objects.get(Email=email)
    msg="Data deleted successfully"
    return render(request, 'dashboard.html', {'admin_user':data, 'tododate':taskdata, 'key1':msg})

def updatedata(request):
    Todotask=Todolist.objects.get(id=request.POST.get('id'))
    email=Todotask.Email
    Todotask.id=request.POST.get('id')
    Todotask.Title=request.POST.get('title')
    Todotask.Task=request.POST.get('task')
    Todotask.Date = datetime.now()
    Todotask.Email=request.POST.get('email')
    Todotask.save()
    taskdata=Todolist.objects.filter(Email=email)
    data=RegistrationModel.objects.get(Email=email)
    msg="Data update Successfully"
    return render(request, 'dashboard.html', {'admin_user':data, 'tododate':taskdata, 'key1':msg })

# ========================= ENDing admin Dashboard (Todo task CRUD) =======================================

# ========================= Starting Admin Dashboard (Product CRUD) ========================================

def product_show1(request):
    data={}
    data['Name']=request.session['Name']
    data['Email']=request.session['Email']
    data['Number']=request.session['Number']
    data['Password']=request.session['Password']
    pro_data1=Productmodel.objects.all()
    print(pro_data1.values())
    Context={
        'admin_user':data, 
        'prop':pro_data1, 
        'media_url': settings.MEDIA_URL
    }
    return render(request, 'productdata.html', Context)

# ================ ENDing Admin Dashboard (Product CRUD) ======================

#=================== User Dashboard login after Navition =============
# def home(request):
#     return render(request, 'index.html', {'user_name':user_info})

# def about1(request):
#     print(request.POST)
#     email=request.POST.get('email')
#     data=RegistrationModel.objects.get(Email=email)
#     return render(request, 'about.html', {'user_name':user_info})

# def contact1(request):
#     print(request.POST)
#     email=request.POST.get('email')
#     data=RegistrationModel.objects.get(Email=email)
#     return render(request, 'contact.html', {'user_name':user_info})

# def product1(request):
#     print(request.POST)
#     email=request.POST.get('email')
#     data=RegistrationModel.objects.get(Email=email)
#     return render(request, 'product.html', {'user_name':user_info})

# def men1(request):
#     print(request.POST)
#     email=request.POST.get('email')
#     data=RegistrationModel.objects.get(Email=email)
#     data1=Productmodel.objects.filter(Prod_Name="Men")
#     print(data)
#     Context={
#         'user_name':user_info, 
#         'prop':data1,
#         'media_url': settings.MEDIA_URL
#     }
#     return render(request, 'men.html',Context )

# def women1(request):
#     print(request.POST)
#     email=request.POST.get('email')
#     data=RegistrationModel.objects.get(Email=email)
#     return render(request, 'women.html', {'user_name':user_info})

# def girl1(request):
#     print(request.POST)
#     email=request.POST.get('email')
#     data=RegistrationModel.objects.get(Email=email)
#     return render(request, 'girl.html', {'user_name':user_info})