"""W URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import os
from django.shortcuts import HttpResponse,render,redirect
import random
import subprocess

def generate_code():
    seeds = "1234567890"
    random_str = []

    for i in range(6):
        random_str.append(random.choice(seeds))

    return "" . join(random_str)



import datetime
def makedir():
    uid = generate_code()
    now = datetime.datetime.now()
    struid = now.strftime("%Y%m%d%H%M%S") + uid
    print(struid)
    # location = "temp/Inputdata/"+struid
    location = "temp/Inputdata/" + struid
    print(location)
    if not os.path.exists(location):
        os.makedirs(location)
        #print("S")
    return struid

def Server(request):

    file = request.FILES.get("fileSeq", None)
    print(type(file))
    flag = False
    if file: flag=True
    #print("sdasd",file.name)
    if request.method == "POST" and flag ==True:
        flag=False
        struid = makedir()
        file_path = "../W/temp/Inputdata/" + struid

        destination = open(os.path.join(file_path,file.name), 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
        #print(request.FILES)
        os.chdir("../EnACP-master")
        subprocess.check_call('python EnACP_Predict.py '+os.path.join(file_path,file.name))
        os.chdir("E:\W")
        return render(request,'Result.html')
    return render(request,'Server.html')

def Result(reuqest):
    return render(reuqest,'Result.html')

urlpatterns = [
    #path('admin/', admin.site.urls),
    url('Server/', Server),
    url('Result/',Result)

]

