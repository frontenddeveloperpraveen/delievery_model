from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
import random
import smtplib
import qrcode
from .models import Order
import json
from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent

BASE_URL = 'https://127.0.0.1:8080/'

def Home(request):

    return HttpResponse("Hi Bro")

def random_num():return random.randint(1111111111,9999999999)


def Gen(request):

    name = request.GET['name']
    price = request.GET['price']
    email = request.GET['email']

    print(name,price,email)

    while True:
        ordernum = random_num()
        if (Order.objects.filter(orderid = ordernum).exists() == False):
            break
    
    url = BASE_URL+"/validate/"+str(ordernum)

    img = qrcode.make(url)
    img.save('static/'+(str(ordernum)+'.jpg'))
    Order.objects.create(orderid = ordernum,name=name,price=price,email=email)
    print(ordernum)
    return render(request, 'display.html', {'img': ordernum})

def space(request):

    return render(request,'qr.html')

def validate(request,orderid):
    if Order.objects.filter(orderid=orderid).exists():
        order = Order.objects.filter(orderid=orderid).first()
        if order.verified == False:
            otp = random.randint(1111,9999)
            print(otp)
            # Email configuration
            smtp_server = "smtp.gmail.com" 
            smtp_port = 587 
            sender_email = "order.bytecamp@gmail.com"  # Replace with your email address
            sender_password = "hdjudvhtnjxwihbv"  # Replace with your email password
            recipient_email = order.email  # Replace with the recipient's email address
            subject = "OTP - ORDER DELIEVERY CONFIRMATION"
            message = f'''
Dear {order.name},
Your OTP : {otp}
Get your package by conveying the OTP above to complete the Order. Never Share OTP to anyone other than authorised Persons,
Regards,
Praveen KR
(Developer)
Founder of Byte Camp
            '''
            try:
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                server.login(sender_email, sender_password)

                # Compose the email
                email = f"Subject: {subject}\n\n{message}"

                # Send the email
                server.sendmail(sender_email, recipient_email, email)
                print("Email sent successfully!")

            except Exception as e:
                print(f"An error occurred: {e}")

            finally:
                # Quit the SMTP server
                server.quit()

            return render(request,'otp.html',{'otp':otp, 'orderid':orderid})
        else:
            return HttpResponse("QR Code Expired")
    
    else:
        return HttpResponse("Wrong QR code")

def confirm(request):
    post_data_text = request.body.decode('utf-8')
    print(post_data_text)
    post_data = json.loads(post_data_text)
    msg = post_data.get('message')
    orderid = post_data.get('orderid')
    if msg == "A875ha87saxhba7'''///jkxhjba,[]ASMJAJBJ" :
        if Order.objects.filter(orderid=orderid).exists:
            order = Order.objects.filter(orderid=orderid).first()
            order.verified = True
            order.save()
            path = 'static/' + orderid + '.jpg'

            try:
                os.remove(path)
            except Exception as e:
                # Handle the exception, e.g., log it or print an error message
                print(f"Error deleting file {path}: {e}")

            try:
                # Assuming 'orderid' is a unique identifier in your Order model
                order_to_delete = Order.objects.get(orderid=orderid)
                name = order_to_delete.name
                print(name)
                email = order_to_delete.email
                print(email)
                order_to_delete.delete()
            except Order.DoesNotExist:
                # Handle the case where the order with the given ID doesn't exist
                print(f"Order with orderid {orderid} does not exist")
            except Exception as e:
                # Handle other exceptions, e.g., database errors
                print(f"Error deleting order with orderid {orderid}: {e}")
            smtp_server = "smtp.gmail.com" 
            smtp_port = 587 
            sender_email = "order.bytecamp@gmail.com"  # Replace with your email address
            sender_password = "hdjudvhtnjxwihbv"  # Replace with your email password
            recipient_email = email  # Replace with the recipient's email address
            subject = "Order Delievered Successfully"
            message = f'''
Dear {name},
Congratulations, Your Package has been Delieved successfully at your doorstep.
Thank you for choosing us for your purchase. Looking Foward to you serve you again.
Regards,
Praveen KR
(Developer)
Founder of Byte Camp
            '''
            try:
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                server.login(sender_email, sender_password)

                # Compose the email
                email = f"Subject: {subject}\n\n{message}"

                # Send the email
                server.sendmail(sender_email, recipient_email, email)
                print("Email sent successfully!")

            except Exception as e:
                print(f"An error occurred: {e}")

            finally:
                # Quit the SMTP server
                server.quit()
            return JsonResponse({"msg":"Order Delievery Confirmation Approved. You can Deliever the Package to the Customer"})
        else:
            return JsonResponse({"msg":"Session Breakout - Malious Activity Deducted"})
    else:
         return JsonResponse({"msg":"Session Breakout - Malious Activity Deducted"})