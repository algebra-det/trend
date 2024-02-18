from django.shortcuts import render, redirect, get_object_or_404
from .models import MyUser
from core.models import Profile, UserGame
from .forms import UserAddForm, UserNormalAddForm, UserChangeAdminForm, UserChangeNormalForm

from django.contrib import messages

from trend.decorators import admin_only

from trend import utils


districts_dict = utils.get_districts_dict()

# districts_dict = {
#     'Lombardy': {
#         'latitude': 45.585556,
#         'longitude': 9.930278,
#     },
#     'Non Valley': {
#         'latitude': 46.337353,
#         'longitude': 11.057293
#     }
# }


# Admin Users

@admin_only
def admin_users(request):
    users = MyUser.objects.filter(is_admin=True)
    context = {
        'users': users,
        'what': 'admin'
    }
    return render(request, 'account/admin_users.html', context)

@admin_only
def create_admin(request):
    if request.method == 'POST':
        form = UserAddForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_admin = True
            user.is_staff = False
            user.save()
            profile = Profile.objects.create(user=user)
            profile.save()
            usergame = UserGame.objects.create(profile=profile)
            usergame.save()
            messages.success(request, f"L'utente è stato creato con successo!")
            return redirect('account:admin_users')
    
    else:
        form = UserAddForm()
    context = {
        'form': form,
        'admin_active': True
    }
    return render(request, 'account/create_admin_user.html', context)




# Normal Users
@admin_only
def users(request):
    users = MyUser.objects.filter(is_admin=False)
    context = {
        'users': users,
        'user_active': True
    }
    return render(request, 'account/users.html', context)

@admin_only
def create_user(request):
    if request.method == 'POST':
        form = UserNormalAddForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff=False
            user.save()
            profile = Profile.objects.create(user=user)
            
            profile.latitude = districts_dict[user.province]['latitude']
            profile.longitude = districts_dict[user.province]['longitude']
            profile.save()

            usergame = UserGame.objects.create(profile=profile)
            usergame.save()
            messages.success(request, f"L'utente è stato creato con successo!")
            return redirect('account:users')
    
    else:
        form = UserNormalAddForm()
    context = {
        'form': form,
        'user_active': True
    }
    return render(request, 'account/create_user.html', context)




def admin_or_not(user):
    if user.is_superuser:
        return 'admin'
    else:
        return 'norm'

@admin_only
def edit(request, id):
    user = get_object_or_404(MyUser, pk=id)
    if request.method == 'POST':
        if user.is_staff:
            form = UserChangeAdminForm(request.POST, instance=user)
            if form.is_valid():
                user = form.save()
                messages.success(request, f"L'utente è stato modificato con successo!")
                return redirect('account:admin_users')
            else:
                messages.error(request, 'Something went wrong' )
                return redirect('account:admin_users')
        else:
            form = UserChangeNormalForm(request.POST, instance=user)
            if form.is_valid():
                user = form.save()
                profile = user.profile
                profile.latitude = districts_dict[user.province]['latitude']
                profile.longitude = districts_dict[user.province]['longitude']
                profile.save()
                messages.success(request, f"L'utente è stato modificato con successo!")
                return redirect('account:users')
            else:
                messages.error(request, 'Something went wrong' )
                return redirect('account:users')
    
    else:
        if user.is_staff:
            form = UserChangeAdminForm(instance=user)
            context = {
                'form': form,
                'what': admin_or_not(user)
            }
            return render(request, 'account/edit_user_admin.html', context)
        else:
            form = UserChangeNormalForm(instance=user)
            context = {
                'form': form,
                'what': admin_or_not(user)
            }
            return render(request, 'account/edit_user.html', context)

@admin_only
def delete(request, id):
    user = get_object_or_404(MyUser, pk=id)
    if request.method == 'POST':
        if user.is_superuser:
            user.delete()
            return redirect('account:admin_users')
        user.delete()
        return redirect('account:users')

    context = {
        'user': user,
        'what': admin_or_not(user)
    }
    return render(request, 'account/delete.html', context)

