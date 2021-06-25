from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from chat.nlp import start_chat_msg
from chat.models import SavedChat
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone

def is_participant(user):
    return user.groups.filter(name='participant').exists()


def is_oz(user):
    return user.groups.filter(name='oz').exists()


# General views
def index(request):
    group_list=[]
    for g in request.user.groups.all():
        group_list.append(g.name)
    data = {'groups': group_list}
    return render(request, 'chat/index.html', data)


# Participant views
@user_passes_test(is_participant)
def start(request):
    request.session['ws_group_name'] = request.user.username  # websocket group name is participant username
    t = SavedChat(
        ws_group_name=request.user,
        chat_data=str([start_chat_msg()])
        )
    t.save()
    request.session['chat_pk'] = t.pk
    return render(request, 'chat/start.html')


@user_passes_test(is_participant)
def interface(request):
    trial_id = request.POST['trial_id']
    if trial_id == "":
        trial_id = "unspecified"
    SavedChat.objects.filter(pk=request.session['chat_pk']).update(trial_id=trial_id)
    return render(request, 'chat/interface.html', {'start_chat_msg': start_chat_msg()})


# Oz views
@user_passes_test(is_oz)
def ozstart(request):
    # Get all logged in users
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    uid_list = []
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))
    all_logged_in_users = User.objects.filter(id__in=uid_list)
    all_logged_in_usernames = []
    for user in all_logged_in_users:
        all_logged_in_usernames.append(user.username)
    all_logged_in_usernames.remove(request.user.username) # comment out to test with self
    return render(request, 'chat/ozstart.html', {'users': all_logged_in_usernames})


@user_passes_test(is_oz)
def ozinterface(request):
    try:
        request.session['ws_group_name'] = request.POST['ws_group_name']
        request.session['supervisor_role'] = request.POST['supervisor_role']
        request.session['chat_pk'] = SavedChat.objects.filter(ws_group_name=request.session['ws_group_name']).latest('timestamp_start').pk
        request.session['trial_id'] = SavedChat.objects.get(pk=request.session['chat_pk']).trial_id
        SavedChat.objects.filter(pk=request.session['chat_pk']).update(supervisor_role=request.session['supervisor_role'])
    except:
        return redirect('/chat/ozstart')
    else:
        return render(request, 'chat/ozinterface.html',
                      {'start_chat_msg': start_chat_msg(),
                       'participant_name': request.session['ws_group_name'],
                       'supervisor_role': request.session['supervisor_role'],
                       'trial_id': request.session['trial_id']
                       }
                      )
