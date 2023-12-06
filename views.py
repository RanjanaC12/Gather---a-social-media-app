from django.shortcuts import render
from django.db import IntegrityError
from Users.models import Users_table
from Users.models import Posts,Friends,Comments,Requests
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password  
import datetime
from pathlib import Path

from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages

import random
import string

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent


def Users(request):
    if request.method== "POST" :
        try:
            if request.POST.get('password2')== request.POST.get('password'):
                allusers=Users_table.objects.all()
                flag=0
                for i in range(0,len(allusers)):
                    if allusers[i].email == request.POST.get('email'):
                        flag=1
                        break
                if flag==1:
                    return render(request,"register.html",{'error':'This email id is already registered !'})
                else:
                    auser = Users_table(username=request.POST.get('username'),email=request.POST.get('email'),password=make_password(request.POST.get('password')),college=request.POST.get('college'),course=request.POST.get('course'),date=request.POST.get('date'),gender=request.POST.get('gender'),images=request.FILES.get('image'),phone=request.POST.get('number'))
                    auser.save();
                    return render(request,"register.html",{'info':'The user '+request.POST.get('username')+' has been registered successfully'})
            else:
                return render(request,"register.html",{'error':'Password Mismatch !'})
        except IntegrityError:
            return render(request,"register.html",{'error':'The user '+request.POST.get('username')+' exits !'})
    else:
        return render(request,"register.html")

# Create your views here.
def Login(request):
    
    global user_email;
    global user_photo;
    global allposts2;
    global user_name;
    global allusers;
    global comments2;
    if request.method == 'POST':
        print(BASE_DIR)
        allposts = Posts.objects.all()
        friends = Friends.objects.all()
        friends2=[]
        for i in range(0,len(friends)):
            if friends[i].email1_id == request.POST.get('email'):
                friends2.append(friends[i].email2)
        
        comments2=Comments.objects.all()
        allposts2=[]
        
        for i in range(0,len(allposts)):
            
            if allposts[i].email.email in friends2:
                
                allposts2.append(allposts[i])
        
        allusers=Users_table.objects.all()
        flag=0
        for i in range(0,len(allusers)):
           
            if check_password(request.POST.get('password'),allusers[i].password)  and allusers[i].email==request.POST.get('email'):
               flag=flag+1
               user_email = request.POST.get('email');
               user_photo = allusers[i].images;
               user_name=allusers[i].username;
               return render(request,"dashboard.html",{'comments':comments2,'allusers':allusers,'info2':request.POST.get('email'),'info':user_name,'img_obj':user_photo,'allposts':allposts2})
        if flag==0:
            return render(request,"login.html",{'info':'Incorrect username or password !'})
    else:
        return render(request,"login.html")
    

def Add_post(request):
    if request.method == 'POST':
        mypost2 = str(request.FILES.get('mypost'))
        mypost = request.FILES.get('mypost')
        mycap=''
        if len(request.POST.get('caption'))!= 0:
            mycap = request.POST.get('caption')
        date2 = datetime.datetime.now()
        allusers=Users_table.objects.all()
        comments2=Comments.objects.all()
        
        category = 'image'
        if mypost2.endswith('.mp4') or mypost2.endswith('.MP4'):  
            category = 'video'
        for i in range(0,len(allusers)):
            if allusers[i].email==user_email:
                apost=Posts(email=allusers[i],username = allusers[i].username,date=date2,posts=mypost,caption=mycap,total_likes =0)
                apost.save();
                return render(request,"makepost.html",{'category':category,'comments':comments2,'allusers':allusers,'info':user_name,'allposts':allposts2,'img_obj':user_photo,'my_post':request.FILES.get('mypost')})
    else:
        allusers=Users_table.objects.all();
        comments2=Comments.objects.all();
        return render(request,"makepost.html",{'comments':comments2,'allusers':allusers,'info':user_name,'img_obj':user_photo,'allposts':allposts2})
    
def Search_friend(request):
    global allusers2;
    comments2=Comments.objects.all()
    allusers=Users_table.objects.all()
    if request.method == 'POST':
        college2=request.POST.get('college')
        course2 = request.POST.get('course')
        allusers = Users_table.objects.all()
        allusers2=[]
        friend_list=Friends.objects.all()
        friend_list2=[]
        for i in range(0,len(friend_list)):
            if friend_list[i].email1_id == user_email:
                friend_list2.append(friend_list[i].email2)
        allreq=Requests.objects.all()
        req_list=[]
        for i in range(0,len(allreq)):
            if allreq[i].email2==user_email:
                req_list.append(allreq[i].email1.email)
        for i in range(0,len(allusers)):
            if allusers[i].college == college2 and allusers[i].course == course2 and allusers[i].email != user_email:
                if allusers[i].email not in friend_list2 and allusers[i].email not in req_list:
                    allusers2.append(allusers[i])
        return render(request,'search_friends.html',{'comments':comments2,'allusers':allusers,'info':user_name,'allusers2':allusers2,'img_obj':user_photo,'allposts':allposts2})
    else:
        return render(request,'search_friends.html',{'comments':comments2,'allusers':allusers,'info':user_name,'img_obj':user_photo,'allposts':allposts2})
    
    
def Add_friend(request):
    allposts = Posts.objects.all()
    allposts2=[]
     
    friends = Friends.objects.all()
    friends2=[]
    for i in range(0,len(friends)):
        if friends[i].email1_id == user_email:
            friends2.append(friends[i].email2)  
    for i in range(0,len(allposts)):
        if allposts[i].email.email in friends2:
            allposts2.append(allposts[i])
    if request.method=='POST':
        allusers=Users_table.objects.all() 
        for i in range(0,len(allusers)):
            if allusers[i].email==request.POST.get('friend'):
                x=Requests(email1=allusers[i],email2=user_email)
                x.save()
                
                for j in range(0,len(allusers2)):
                    if allusers2[j].email == request.POST.get('friend'):
                        allusers2.remove(allusers2[j])
                        break
               
                
                

        return render(request,'search_friends.html',{'comments':comments2,'allusers':allusers,'info':user_name,'allusers2':allusers2,'img_obj':user_photo,'allposts':allposts2})
    else:
        return render(request,'search_friends.html',{'comments':comments2,'allusers':allusers,'info':user_name,'allusers2':allusers2,'img_obj':user_photo,'allposts':allposts2})






def view_requests(request):
    allusers2=Users_table.objects.all()
    req=Requests.objects.all();
    req2=[]
    for i in range(0,len(req)):
        if req[i].email1_id==user_email and req[i].status =='unconfirmed':
            req2.append(req[i])
    
    return render(request,'friend_req.html',{'requests':req2,'comments':comments2,'allusers':allusers,'info':user_name,'allusers2':allusers2,'img_obj':user_photo,'allposts':allposts2})

def accept_requests(request):
    allusers2=[]
    global allposts2
    allusers=Users_table.objects.all()
    friends =Friends.objects.all() 
    allreq=Requests.objects.all()
    comments2=Comments.objects.all()
    for i in range(0,len(friends)):
            if friends[i].email1_id == user_email:
                allusers2.append(friends[i].email2)
    if request.method=='POST':
        
        for i in range(0,len(allusers)):
            if allusers[i].email== request.POST.get('reqfriend'):
                x=Friends(email1=allusers[i],email2=user_email)
                y = Friends(email1_id= user_email,email2=request.POST.get('reqfriend'))
                y.save()
                x.save()
        for i in range(0,len(allreq)):
            if allreq[i].email1_id==user_email and allreq[i].email2 == request.POST.get('reqfriend'):
                
                Requests.objects.filter(rid=allreq[i].rid).delete()
                break
        req=Requests.objects.all()
        req2=[]
        for i in range(0,len(req)):
            if req[i].email1_id==user_email:
                req2.append(req[i])
        allposts = Posts.objects.all()
        friends = Friends.objects.all()
        friends2=[]
        for i in range(0,len(friends)):
            if friends[i].email1_id == user_email:
                friends2.append(friends[i].email2)
        
        
        comments2=Comments.objects.all()
        allposts2=[]
        
        for i in range(0,len(allposts)):
            
            if allposts[i].email.email in friends2:
                
                allposts2.append(allposts[i])
        
        
    
        return render(request,'friend_req.html',{'requests':req2,'comments':comments2,'allusers':allusers,'info':user_name,'allusers2':allusers2,'img_obj':user_photo,'allposts':allposts2})
    else:
        req=Requests.objects.all()
        req2=[]
        for i in range(0,len(req)):
            if req[i].email1_id==user_email:
                req2.append(req[i])
        return render(request,'friend_req.html',{'requests':req2,'comments':comments2,'allusers':allusers,'info':user_name,'allusers2':allusers2,'img_obj':user_photo,'allposts':allposts2})
    
def reject_request(request):
    
    allusers2=[]
    allusers=Users_table.objects.all()
    friends =Friends.objects.all() 
    allreq=Requests.objects.all()
    comments2=Comments.objects.all()
    for i in range(0,len(friends)):
        if friends[i].email1_id == user_email:
            allusers2.append(friends[i].email2)
    if request.method=='POST':
        for i in range(0,len(allreq)):
            if allreq[i].email1_id==user_email and allreq[i].email2 == request.POST.get('reqfriend'):
                Requests.objects.filter(rid=allreq[i].rid).delete()
                break
        req=Requests.objects.all()
        req2=[]
        for i in range(0,len(req)):
            if req[i].email1_id==user_email:
                req2.append(req[i])
        return render(request,'friend_req.html',{'requests':req2,'comments':comments2,'allusers':allusers,'info':user_name,'allusers2':allusers2,'img_obj':user_photo,'allposts':allposts2})
    else:
        req=Requests.objects.all()
        req2=[]
        for i in range(0,len(req)):
            if req[i].email1_id==user_email:
                req2.append(req[i])
        return render(request,'friend_req.html',{'requests':req2,'comments':comments2,'allusers':allusers,'info':user_name,'allusers2':allusers2,'img_obj':user_photo,'allposts':allposts2})
    






def Add_comment(request):
    if request.method=='POST':
        val = request.POST.get('comment')
        postid=Posts.objects.all()
        for i in range(0,len(postid)):
            if str(postid[i].post_id)==request.POST.get('pid'):
                postid=postid[i]
                break
        
        for i in range(0,len(allusers)):
            if allusers[i].email==user_email:
                user_email2=allusers[i];
        date2=datetime.datetime.now()
        c=Comments(category='comment',comment=val,post_id=postid,email=user_email2,date=date2)
        c.save();
        comments2=Comments.objects.all();
        
        return render(request,'dashboard.html',{'comments':comments2,'allusers':allusers,'info2':user_email,'info':user_name,'img_obj':user_photo,'allposts':allposts2})
    else:
        return render(request,'dashboard.html',{'comments':comments2,'allusers':allusers,'info2':user_email,'info':user_name,'img_obj':user_photo,'allposts':allposts2})

def Add_like(request):
    
    if request.method=='POST':
        flag=0
        
        comments2=Comments.objects.all()
        for i in range(0,len(comments2)):
            
            if comments2[i].email_id == user_email:
                
                if comments2[i].category == 'like':
                  
                  if comments2[i].post_id_id == int(request.POST.get('pid')):
                        
                        flag=1
                        break
        if flag==0:
            
            postid=Posts.objects.all()
            for i in range(0,len(postid)):
                if str(postid[i].post_id)==request.POST.get('pid'):
                    postid[i].total_likes= postid[i].total_likes +1
                    postid[i].save()
                    
                    postid=postid[i]
                    break
            for i in range(0,len(allusers)):
                if allusers[i].email==user_email:
                    user_email2=allusers[i]; 
            c=Comments(category='like',comment='This post was liked',post_id=postid,email=user_email2)
            c.save()
            comments2=Comments.objects.all()
        return render(request,'dashboard.html',{'comments':comments2,'allusers':allusers,'info2':user_email,'info':user_name,'img_obj':user_photo,'allposts':allposts2})
    else:
        return render(request,'dashboard.html',{'comments':comments2,'allusers':allusers,'info2':user_email,'info':user_name,'img_obj':user_photo,'allposts':allposts2})

def check_friends(request):
    
    allusers2=[]
    allusers=Users_table.objects.all()
    friends =Friends.objects.all() 
    comments2=Comments.objects.all()
    my_friends=[]
    for i in range(0,len(friends)):
        if friends[i].email1_id == user_email:
            allusers2.append(friends[i].email2)
    
    for i in range(0,len(allusers2)):
        for j in range(0,len(allusers)):
            if allusers2[i] == allusers[j].email:
                my_friends.append(allusers[j])
    
    return render(request,"check_friends.html",{'my_friends':my_friends,'comments':comments2,'allusers':allusers,'info2':user_email,'info':user_name,'img_obj':user_photo,'allposts':allposts2})

def view_profile(request):
    allusers2=[]
    allusers=Users_table.objects.all()
    friends =Friends.objects.all() 
    allposts3 = Posts.objects.filter(email_id = user_email)
    comments2=Comments.objects.all()
    
    for i in range(0,len(friends)):
        if friends[i].email1_id == user_email:
            allusers2.append(friends[i].email2)

    for i in range(0,len(allusers)):
        if allusers[i].email==user_email:
            break
    
    return render(request,'view_profile.html',{'my_posts':allposts3,'my_profile':allusers[i],'comments':comments2,'allusers':allusers,'info2':user_email,'info':user_name,'img_obj':user_photo,'allposts':allposts2})

def edit_profile(request):
    global user_photo
    allusers2=[]
    allusers=Users_table.objects.all()
    friends =Friends.objects.all() 
    comments2=Comments.objects.all()
    
    for i in range(0,len(friends)):
        if friends[i].email1_id == user_email:
            allusers2.append(friends[i].email2)
    for i in range(0,len(allusers)):
            if allusers[i].email == user_email:
                break
    user_photo=allusers[i].images
    if request.method=='POST':
        
        if request.POST.get('my_date') != '':
            #bool function checks if objects is empty
            allusers[i].date=request.POST.get('my_date')
        if  bool(request.POST.get('my_gender')):
            allusers[i].gender=request.POST.get('my_gender')
        if  bool(request.POST.get('my_clg')):
            allusers[i].college = request.POST.get('my_clg')
        if  bool(request.POST.get('my_course')):
            allusers[i].course = request.POST.get('my_course')
        if  bool(request.POST.get('my_phone')):
            allusers[i].phone = request.POST.get('my_phone')
        if  bool(request.FILES.get('my_img')):
            print("Hi")
            allusers[i].images = request.FILES.get('my_img')
        allusers[i].save();
        user_photo= allusers[i].images
        return render(request,'edit_profile.html',{'my_profile_update':'Update Successful','comments':comments2,'allusers':allusers,'info2':user_email,'info':user_name,'img_obj':user_photo,'allposts':allposts2})
    else:
        return render(request,'edit_profile.html',{'comments':comments2,'allusers':allusers,'info2':user_email,'info':user_name,'img_obj':user_photo,'allposts':allposts2})
     
      
def del_friend(request):
    allusers2=[]
    allusers=Users_table.objects.all()
    friends =Friends.objects.all() 
    comments2=Comments.objects.all()
    my_friends=[]
    for i in range(0,len(friends)):
        if friends[i].email1_id == user_email:
            allusers2.append(friends[i].email2)
    
    for i in range(0,len(allusers2)):
        for j in range(0,len(allusers)):
            if allusers2[i] == allusers[j].email:
                my_friends.append(allusers[j])
    if request.method == 'POST':
        for i in range(0,len(friends)):
         if friends[i].email1_id == user_email and friends[i].email2 == request.POST.get('my_friend'):
            Friends.objects.filter(fid = friends[i].fid).delete()
         if friends[i].email1_id == request.POST.get('my_friend') and friends[i].email2 == user_email:
            Friends.objects.filter(fid = friends[i].fid).delete()
        my_friends=Friends.objects.filter(email1_id = user_email)
        
    return render(request,"check_friends.html",{'my_friends':my_friends,'comments':comments2,'allusers':allusers,'info2':user_email,'info':user_name,'img_obj':user_photo,'allposts':allposts2})


def forgot(request):
    return render(request,'forgot.html')


def generate_random_string():
    length = random.randint(5, 8)  # Random length between 5 and 8
    characters = string.ascii_letters + string.digits + string.punctuation  # Special characters, numbers, and capital letters
    return ''.join(random.choice(characters) for _ in range(length))

# Example usage
random_string = generate_random_string()

def forgotpasswordprocess(request):
    print(request.POST)
    user_email = request.POST['useremail']
    try:
        db_data = Users_table.objects.get(email=user_email)
        # Fetch password from db_data
        db_data.password=make_password(random_string)
        db_data.save();
        subject = 'Forgot Password'
        message = ' Your Password is  ' + random_string
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user_email,]
        send_mail(subject, message, email_from, recipient_list)
        messages.success(request, 'Password sent to email')
        return redirect('Login')  # Replace with the correct URL pattern name for login
    except Users_table.DoesNotExist:
        messages.error(request, 'Wrong email details')
        return render(request, 'forgot.html')  # Render the forgot.html template with an error messages