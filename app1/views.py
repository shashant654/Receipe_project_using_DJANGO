from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout 
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator



# Create your views here.
@login_required(login_url='/login/')
def receipes(request):
    if request.method == "POST":

          data = request.POST
          receipe_image = request.FILES.get('receipe_image')
          receipe_name = data.get('receipe_name')
          receipe_description = data.get('receipe_description')

          # print(receipe_description)
          # print(receipe_name)
          # print(receipe_image)

          Receipe.objects.create(
                    receipe_image = receipe_image,
                    receipe_name = receipe_name,
                    receipe_description = receipe_description,
          )

          return redirect('/receipes')
      

    queryset = Receipe.objects.all()

    if request.GET.get('search'):
       queryset = queryset.filter(receipe_name__icontains = request.GET.get('search'))


    context = {'receipes':queryset}
    return render(request,'receipes.html',context)

@login_required(login_url='/login/')
def delete_receipe(request,id):
      # return redirect('/receipes/')
      # print(id)
      queryset = Receipe.objects.get(id = id)
      queryset.delete()
      return redirect('/receipes/')

@login_required(login_url='/login/')
def update_receipe(request,id):
      queryset = Receipe.objects.get(id = id)

      if request.method == "POST":
            data = request.POST

            receipe_image = request.FILES.get('receipe_image')
            receipe_name = data.get('receipe_name')
            receipe_description = data.get('receipe_description')

            queryset.receipe_name = receipe_name
            queryset.receipe_description = receipe_description

            if receipe_image:
                  queryset.receipe_image = receipe_image
            
            queryset.save()
            return redirect('/receipes/')

      context = {'receipe': queryset}

      return render(request,'update_receipes.html',context)
      

def login_page(request):

      if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            if not User.objects.filter(username= username).exists():
                  messages.error(request, 'Invalid Username')
                  return redirect('/login/')

            user = authenticate(username = username,password=password)      

            if user is None:
                  messages.error(request, 'Invalid Password')
                              # password = password such like this we can't encrypt password becoz ye string hota hai
                  return redirect('/login/')

            else:
                  login(request, user)    
                  # jo user login kiya hai use hi sesseion m dalna hoga that's why login() function me active user ko dala hu
                  return redirect('/receipes/')  


      return render(request,'login.html')

# first of all check kiye ki username exist krte hai ya ni agr exist ni krte hai toh invalid username show kr dega and redirect kr denge login page pe hi

# jbb username check ho jaye toh password check krenge jo ki authenticate fxn k through check hota hai agr ye NONE return kre toh Ivalid password show kr dega else login session me chla jayega and redirect kr denge receipes page pe
       


def logout_page(request):
      logout(request)
      return redirect('/login/')


def register(request):

      if request.method == "POST":
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = User.objects.filter(username = username)

            if user.exists():
                  messages.info(request,'username already taken')
                  return redirect('/register/')

            user = User.objects.create(
                  first_name = first_name,
                  last_name = last_name,
                  username = username,
            )
                                                                  
            user.set_password(password)
            user.save()

            messages.info(request,'Account created successfully')

            return redirect('/register/')
      
      return render(request,'register.html')



# ---------------------------------------------------------------

# def get_students(request):
#       queryset = Student.objects.all()
#       contact_list = Contact.objects.all()
#       paginator = Paginator(contact_list, 25)  # Show 25 contacts per page.

#       page_number = request.GET.get("page")
#       page_obj = paginator.get_page(page_number)

#       return render(request, 'report/students.html', {'queryset' : queryset})



