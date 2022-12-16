from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.http import HttpResponse
from django.http import FileResponse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate,login,logout
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .forms import UploadFileForm
from json import dumps

#Added for LAB EXAM then head to createuser , events
from django.conf import settings
from django.core.mail import send_mail


# Create your views here.
def loginpage(request):
    if(request.method =='POST'):
        user = authenticate(username=request.POST['u'], password=request.POST['p'])
        if user is not None:
            login(request,user)
            return redirect('/home')
        else:
            messages.info(request,'invalid credentials!')
            return redirect('/')
    # No backend authenticated the credentials
    else:
        return(render(request,'loginpage.html'))

def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST,request.FILES)
        file = request.FILES['file']
        file.save()
        return HttpResponse("The name of the uploaded file is" + str(file))
    else:
        form = UploadFileForm()
    return render(request,'upload.html',{'form':form})        

def home(request):
    if request.user.is_superuser:
        return render(request,'adminpage.html')
    elif request.user.role == 'Subcontractor':
        return send_files(request)
    elif request.user.role == 'Auditor':
        #return render(request,'auditpage.html')
        return redirect('aud')

def aud(request):
    udl = list(Subcontractor.subcontractor.all())
    adl = Event.objects.filter(audit_id=request.user.id)
    return render(request,'auditpage.html',{'adl': adl ,'udl': udl}) 


def events(request):
    if (request.method == 'POST'):
        event_name = request.POST['en']
        Aud = request.POST['Auditor']
        sub = request.POST['Subcontractor']
        act_list = request.POST.getlist('checks[]')
        eved = request.POST['date']
        evet = request.POST['time']
       # esdata = Event.objects.create()
       # esdata.save(audit=Aud,sub=sub,)
        a = Auditor.auditor.get(username = Aud)
        s = Subcontractor.subcontractor.get(username = sub)
        '''
        subject = 'AN EVENT HAS BEEN CREATED FOR YOU'
        messageaudit = f'Hi {a.first_name} {a.last_name} , the following are details for your new event : \nEvent name : {event_name}\nSubcontractor name : {s.first_name} {s.last_name} \nDeadline : {evet}\nTo learn more , view events in Brivas Audit Site'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [a.email, ]
        send_mail( subject, messageaudit, email_from, recipient_list )    

        subject = 'AN EVENT HAS BEEN CREATED FOR YOU'
        messagesub = f'Hi {s.first_name} {s.last_name} , the following are details for your new event : \nEvent name : {event_name}\nAuditor name : {s.first_name} {s.last_name} \nDeadline : {evet}\nTo learn more , login in to Brivas Audit Site with your credentials'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [s.email, ]
        send_mail( subject, messagesub, email_from, recipient_list )   
        '''
        #changes made 15-12-22
        newe = Event.objects.create(audit=a,sub=s)
        newe.save()
        print("New event created") 
        for i in act_list:
            newe.acts[i]['selected'] = True
        newe.save()
        #
        return render(request,'adminpage.html')
    else:
        s=Subcontractor.subcontractor.all()
        a=Auditor.auditor.all()
        ac = Act.objects.all()
        return render(request,'createevent.html',{'a': a ,'s': s ,'ac':ac })

def getselected(data):
    act = {}
    for name,parms in data.items():
        if parms['selected'] == True:
            act[name] = parms['uploaded']
    return act
      



def checkevent(request, pk):
    event = Event.objects.get(sub_id = pk)
    data = event.acts
    act = getselected(data)
    print(act)
    print("Event id",type(event.id))
    try:
        files = UploadFile.objects.filter(e_id = event.id)
        for i in files:
            print(i.f_files)
        
    except:
        files = None
        filetry = UploadFile.objects.all()
        for i in filetry:
            print(type(i.e_id_id))
        print("hello")
    if request.method == "POST":
        data = request.POST
        action = data.get("warn")
        observations = request.POST.getlist('message[]')
        actslist = request.POST.getlist('acts[]')
        print(observations,actslist)
        for i,j in event.observation.items():
            if i in actslist:
                index = actslist.index(i)
                event.observation[i] = observations[index]
                print(event.observation[i])
                event.save()

        '''
        if action == "yes":
            subject = 'WARNING : PENDING SUBMISSIONS'
            messagewarn = f'Hi {event.sub.first_name} {event.sub.last_name} ,this is a warning mail , as your event deadline is arroaching soon , please upload the needful at the earliest'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [event.sub.email, ]
            send_mail( subject, messagewarn, email_from, recipient_list )  
        '''  


    return render(request,'aevents.html',{'event':event,'files':files,'act':act})
    



def actmaster(request):
    act = Act.objects.all()
    return render(request,'actmaster.html',{'act': act})

def userlist(request):
    userl = User.objects.all()
    return render(request,'userlist.html',{'userl': userl})    

def newact(request):
    if (request.method == 'POST'):
        act_name = request.POST['actn']
        act_desc = request.POST['actd']
        act_sname = request.POST['actsn']
        actsdata = Act.objects.create(act_name = act_name, act_shname = act_sname,act_desc=act_desc)
        actsdata.save()
        return render(request,'actmaster.html')
    else:
        return render(request,'newact.html')  



def createnewuser(request):
    auditors = User.objects.filter(role='Auditor')
    context = {'auditors':auditors}
    if (request.method == 'POST'):
        print(request.POST['choose'])
        first_name = request.POST['fname']
        last_name =  request.POST['lname']
        username = request.POST['usr']
        email = request.POST['email']
        password1 = request.POST['psw']
        password2 = request.POST['psw-repeat']
        contact_number = request.POST['telphone']
        role = request.POST['choose']
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken!')
                return redirect('createnewuser')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'E-mail Taken!')
                return redirect('createnewuser')
            else:
                print("hey")
                user = User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name,role=role,contact_number=contact_number)
                user.save()
                '''
                subject = 'User Credentials for Brivas Audit Site'
                if role == 'Auditor':
                    message = f'Hi {first_name} {last_name} , welcome to our family !\nStart your auditing journey by using the below credentials\nUSERNAME : {username}\nPASSWORD : {password1}\nROLE : {role}'
                else:
                    message = f'Hello {first_name} {last_name} , we thank you for working with us\nJoin us soon after an event is created for you using the below credentails\nUSERNAME : {username}\nPASSWORD : {password1}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email, ]
                send_mail( subject, message, email_from, recipient_list )
                '''
            
        else:
            messages.info(request,'Password not matching!')
            return redirect('createnewuser')
    
        return redirect('createnewuser')
    else:
        return render(request,'createnewuser.html',context)

def logoutpage(request):
    logout(request)
    return redirect('login')        
'''
def uploadPage(request):
    context = {"data":UploadFile.objects.all()}
    return render(request,'uploadPage.html',context)
'''
def viewprofile(request):
    return render(request,'viewprofile.html')  

def send_files(request):
    
    if request.user.role != 'Subcontractor':
        return HttpResponse('You are not a Subcontractor')
    
    e = Event.objects.get(sub_id = request.user.id)
    data = e.acts
    act = getselected(data)
    print(act)
    try:
            files = UploadFile.objects.filter(e_id = e.id)
            for i in files:
                print(i.f_files)
        
    except:
        files = None
        filetry = UploadFile.objects.all()
        for i in filetry:
            print(type(i.e_id_id))
    context = {'event':Event.objects.get(sub_id = request.user.id),'act':act,'files':files}
    if request.method == "POST":
        name = request.POST.get("filename")
        myfile = request.FILES.get("uploadfile")
        exists = UploadFile.objects.filter(f_files=myfile).exists()
        if exists:
            pass
        else:
            print(e.acts[name]['selected'],e.acts[name]['uploaded'])
            e.acts[name]['uploaded'] = True
            e.save()
            print(e.acts[name]['selected'],e.acts[name]['uploaded'])
            UploadFile(f_name=name,f_files=myfile,e_id_id = e.id).save()
    return render(request,'uploadPage.html',context)


def view_files(request):
    if request.user.role == 'Subcontractor':
        return HttpResponse('You are not an Auditor')
    context = {'event':Event.objects.get(sub_id = request.user.id)}
    if request.method == "GET":
        name = request.GET.get("filename")
        myfile = request.FILES.get("uploadfile")
        UploadFile(f_name=name,f_files=myfile).save()
    return render(request,'uploadPage.html')
