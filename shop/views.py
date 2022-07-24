import os

from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Product, Contact, Orders
from math import ceil
from .models import User
from django.contrib.auth import authenticate, login, logout
from datetime import *
import pickle
import pandas as pd
from datetime import date
import datetime

mealType = None


def train(request):
    import numpy as np

    if os.path.isfile("./trained.sav"):
        print('already trained')
    else:
        print("training")
        dataset = pd.read_csv('Dataset.csv')

        data = dataset.iloc[:, 0:-1].values
        label = dataset.iloc[:, -1].values

        dict = {}
        k = 1
        for item in data:
            if (dict.get(item[0]) == None):
                dict[item[0]] = k
                item[0] = k;
                k = k + 1
            else:
                item[0] = dict[item[0]]

        from sklearn.svm import SVC
        classifier = SVC(kernel='linear', random_state=0)
        classifier.fit(data, label)
        pickle.dump(classifier, open('trained.sav', 'wb'))
    return render(request, 'shop/index.html')


def predict(lastName, dob):
    classifier = pickle.load(open('trained.sav', 'rb'))
    dataset = pd.read_csv('Dataset.csv')
    tempname = len(dataset) + 1
    cnt = 0;
    for item in dataset:
        cnt += 1
        if (item[0] == lastName):
            tempname = cnt
    today = date.today()

    day = datetime.datetime.today().isoweekday()
    dataTemp = [tempname, today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day)),
                datetime.datetime.now().hour,
                day + 1]
    l = [dataTemp]
    temp = classifier.predict(l)
    print(temp)
    global mealType
    mealType = temp[0]


def forcedmeal(request):
    if request.method == 'POST':
        type1 = request.POST['fav_meal']

        global mealType
        if (type1 == 'veg'):
            mealType = 1
        elif (type1 == 'nonveg'):
            mealType = 0
        else:
            mealType = None
        return redirect('home')
    else:
        return HttpResponse('404 - Not Found')


def index(request):
    allProd = []
    catprods = Product.objects.values('mealType', 'id', 'type')
    cats = {item['mealType'] for item in catprods}
    for cat in cats:
        if mealType == None:
            prod = Product.objects.filter(mealType=cat)
        else:
            if mealType == 1:
                prod = Product.objects.filter(mealType=cat, type='veg')
            else:
                prod = Product.objects.filter(mealType=cat, type='nonveg')
        n = len(prod)
        if (n != 0):
            nSlides = (n // 4) + ceil((n / 4) - (n // 4))

            allProd.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProd}
    print(params)
    return render(request, "shop/index.html", params)


def about(request):
    return render(request, "shop/about.html")


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        query = request.POST.get('Query', '')
        contact = Contact(name=name, email=email, phone=phone, Query=query)
        contact.save()
    return render(request, "shop/contact.html")


def checkout(request):
  if request.method == "POST":
        # items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        # phone = request.POST.get('phone', '')

        order = Orders(name=name, email=email, address=address, city=city, state=state,
                       zip_code=zip_code)
        order.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
  return render(request, 'shop/checkout.html')


def search(request):
    if request.method=="POST":
        temp= request.POST.get('search','')

    else:
     return HttpResponse("We are  at Search")


def prodView(request, id):
    product = Product.objects.filter(id=id)
    return render(request, "shop/prodView.html", {'product': product[0]})


def handelSignup(request):
    if request.method == 'POST':
        # Get the post parameters
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        dat = request.POST['dob']
        pass1 = request.POST['psw1']
        pass2 = request.POST['psw2']
        bio = request.POST['bio']
        dat = datetime.datetime.strptime(dat, '%Y-%m-%d').date()
        # checks for empty inputs
        if len(username) > 10:
            messages.error(request, "Username should be less than 10 characters")
            return redirect('home')
        if not username.islower():
            messages.error(request, "Username should be in lower case")
            return redirect('home')
        if dat > date.today():
            messages.error(request, "Date of birth is wrong")
            return redirect('home')
        if not username.isalnum():
            messages.error(request, "Username should only contain alphabets and numbers.")
            return redirect('home')
        if pass1 != pass2:
            messages.error(request, "Passwords should match")
            return redirect('home')

        # create the user
        myuser = User.objects.create_user(email, dat, fname, lname, pass1)

        myuser.save()

        messages.success(request, "Your account has been successfully made")
        return redirect('home')
    else:
        return HttpResponse("Not found")


def handleLogin(request):
    if request.method == 'POST':
        # loginusername
        email = request.POST['email']
        loginpsw = request.POST['loginpsw']

        user = authenticate(email=email, password=loginpsw)
        if user is not None:
            login(request, user)
            predict(user.last_name, user.dob);

            messages.success(request, "You are successfully loged in!!")
            return redirect('home')
        else:
            messages.error(request, "Incorrect Credentials")
            return redirect('home')

    return HttpResponse('404 - Not Found')


def handleLogout(request):
    global mealType
    mealType = None
    logout(request)
    messages.success(request, "You are successfully logged out!!")
    return redirect('home')

# def train(request):
