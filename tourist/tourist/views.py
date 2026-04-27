from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from service.models import  *
from service.blockchain import Blockchain
from service.utils import generate_identity_id
from django.core.exceptions import ObjectDoesNotExist
import numpy as np

blockchain = Blockchain()

def Home(request):
    return render(request,'Home.html', {})

def Panic(request):
    return render(request,'panic.html', {})

def Register(request):

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        tourist_number = request.POST.get("tourist_number")
        guardian_number = request.POST.get("guardian_number")


        # Generate Blockchain ID
        identity_id = generate_identity_id(name, email)

        # Save to database
        Tourist.objects.create(
            name=name,
            email=email,
            password=password,
            tourist_number=tourist_number,
            guardian_number=guardian_number,
            identity_id=identity_id
        )

        return redirect('loginpage')  # important

    return render(request, "Register.html")

def Login(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        user = Tourist.objects.filter(
            email=email,
            password=password
        ).first()

        if user:
            request.session['email'] = email
            return redirect('home')

    return render(request,"Login.html")

def logoutuser(request):
    logout(request)
    return redirect('loginpage')

def Livelocation(request):
    return render(request,'livelocation.html', {})



from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings

import ssl
def emergency_alert(request):
    ssl._create_default_https_context = ssl._create_unverified_context
    if request.method == "POST":
        name = request.POST.get("name")
        location = request.POST.get("location")
        issue = request.POST.get("issue")

        subject = "🚨 Emergency Alert from Tourist"
        message = f"""
        Emergency Alert!

        Name: {name}
        Location: {location}
        Issue: {issue}
        """

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            # 🔴 CHANGE THIS
            ["Prakruthin563@gmail.com"],
            fail_silently=False,
        )

        return render(request, "emergency.html", {"success": True})

    return render(request, "emergency.html")


from django.shortcuts import render

def zones(request):

    # ✅ SAFE ZONES (Tourist + Public Safe Areas)
    safe_zones = [

        # Karnataka (Bangalore)
        {"lat":12.9716,"lng":77.5946,"name":"MG Road","radius":800},
        {"lat":12.9352,"lng":77.6245,"name":"Indiranagar","radius":800},
        {"lat":13.1986,"lng":77.7066,"name":"Kempegowda Airport","radius":1000},

        # Maharashtra (Mumbai)
        {"lat":19.0896,"lng":72.8656,"name":"Mumbai Airport","radius":1000},
        {"lat":18.9217,"lng":72.8347,"name":"Gateway of India","radius":800},
        {"lat":19.2183,"lng":72.9781,"name":"Thane City","radius":800},

        # Delhi
        {"lat":28.5562,"lng":77.1000,"name":"Delhi Airport","radius":1000},
        {"lat":28.6129,"lng":77.2295,"name":"India Gate","radius":800},
        {"lat":28.5245,"lng":77.1855,"name":"Saket","radius":800},

        # Tamil Nadu (Chennai)
        {"lat":12.9941,"lng":80.1709,"name":"Chennai Airport","radius":1000},
        {"lat":13.0827,"lng":80.2707,"name":"Marina Beach","radius":800},
        {"lat":11.0168,"lng":76.9558,"name":"Coimbatore City","radius":800},

        # Telangana (Hyderabad)
        {"lat":17.2403,"lng":78.4294,"name":"Hyderabad Airport","radius":1000},
        {"lat":17.3616,"lng":78.4747,"name":"Charminar","radius":800},
        {"lat":17.3850,"lng":78.4867,"name":"Hitech City","radius":800},

        # West Bengal (Kolkata)
        {"lat":22.6547,"lng":88.4467,"name":"Kolkata Airport","radius":1000},
        {"lat":22.5726,"lng":88.3639,"name":"Park Street","radius":800},

        # Kerala
        {"lat":10.1520,"lng":76.4019,"name":"Cochin Airport","radius":1000},
        {"lat":9.9312,"lng":76.2673,"name":"Kochi City","radius":800},

        # Gujarat
        {"lat":23.0732,"lng":72.6347,"name":"Ahmedabad Airport","radius":1000},
        {"lat":23.0225,"lng":72.5714,"name":"Ahmedabad City","radius":800},

        # Rajasthan
        {"lat":26.8242,"lng":75.8122,"name":"Jaipur Airport","radius":1000},
        {"lat":26.9124,"lng":75.7873,"name":"Jaipur City","radius":800},

        # Uttar Pradesh
        {"lat":26.7606,"lng":80.8893,"name":"Lucknow Airport","radius":1000},
        {"lat":25.3176,"lng":82.9739,"name":"Varanasi","radius":800},

    ]


    # ❌ UNSAFE ZONES (High Traffic / Accident / Routes)
    unsafe_zones = [

        # Bangalore Routes
        {"lat":13.0358,"lng":77.5970,"name":"Hebbal Flyover","radius":1500},
        {"lat":13.1986,"lng":77.7066,"name":"Airport Highway NH44","radius":1500},
        {"lat":12.9275,"lng":77.5830,"name":"Silk Board Junction","radius":1500},

        # Mumbai Routes
        {"lat":19.0896,"lng":72.8656,"name":"Western Express Highway","radius":1500},
        {"lat":18.9750,"lng":72.8258,"name":"Dadar Junction","radius":1500},

        # Delhi Routes
        {"lat":28.5562,"lng":77.1000,"name":"NH48 Airport Road","radius":1500},
        {"lat":28.7041,"lng":77.1025,"name":"Outer Ring Road","radius":1500},

        # Chennai Routes
        {"lat":12.9941,"lng":80.1709,"name":"GST Road Airport Route","radius":1500},
        {"lat":13.0500,"lng":80.2700,"name":"Chennai Central Area","radius":1500},

        # Hyderabad Routes
        {"lat":17.2403,"lng":78.4294,"name":"ORR Airport Route","radius":1500},
        {"lat":17.3850,"lng":78.4867,"name":"Ameerpet Junction","radius":1500},

        # Kolkata
        {"lat":22.6547,"lng":88.4467,"name":"VIP Road Airport Route","radius":1500},

        # Kerala
        {"lat":10.1520,"lng":76.4019,"name":"NH66 Coastal Highway","radius":1500},

        # Gujarat
        {"lat":23.0732,"lng":72.6347,"name":"SG Highway Ahmedabad","radius":1500},

        # Rajasthan
        {"lat":26.8242,"lng":75.8122,"name":"Jaipur Ring Road","radius":1500},

        # UP
        {"lat":26.7606,"lng":80.8893,"name":"Lucknow Ring Road","radius":1500},

    ]

    return render(request, "zones.html", {
        "safe_zones": safe_zones,
        "unsafe_zones": unsafe_zones
    })

def Feedback(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        messages = request.POST['msg']
        ins = Feed(name=name,msg=messages, email=email)
        ins.save()
        print("ok")
    return render(request,'Feedback.html', {})


def dashboard(request):

    email = request.session.get("email")

    if not email:
        return redirect('loginpage')

    tourist = Tourist.objects.filter(email=email).first()

    return render(request, "Dashboard.html", {
        "identity_id": tourist.identity_id
    })
