from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login

# Create your views here.
def index(request):
    return render(request, 'index.html') 

def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)  # Set the chosen password
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user  # Set the one-to-one relation
            profile.save()

            # Log the user in (optional)
            new_user = authenticate(username=user_form.cleaned_data['username'],
                                    password=user_form.cleaned_data['password1'])
            login(request, new_user)
            return redirect('home')  # Redirect to a success page.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })