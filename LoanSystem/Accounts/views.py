from django.shortcuts import render, redirect
from .forms import ProfileForm, RegistrationForm
import sweetify
from django.contrib.auth import login, logout, authenticate


def registeruser(request):
    reg_form = RegistrationForm()
    prof_form = ProfileForm()

    if request.method == "POST":
        reg_form = RegistrationForm(request.POST)
        prof_form = ProfileForm(request.POST, request.FILES)

        if reg_form.is_valid() and prof_form.is_valid():
            user = reg_form.save()
            username = user.username

            profile = prof_form.save(commit=False)
            profile.user = user
            profile.save()
            category = profile.Category

            sweetify.success(request, title="Success",
                             text=f"Account for {username} as {category} Successfully Created",
                             icon="success")
        elif reg_form.errors:
            errors = dict(reg_form.errors)

            for key, value in errors.items():
                value = (value[0])

            sweetify.error(request, title=f'{key}', text=f"{value}", icon="error")
    context = {'reg_form': reg_form, 'prof_form': prof_form}

    return render(request, 'Accounts/login_register.html', context)


def loginuser(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            return redirect('home')
        else:
            sweetify.error(request, title='ERROR', text='USERNAME OR PASSWORD IS INCORRECT', icon='error')

    return render(request, 'Accounts/login_register.html')


def logoutUser(request):
    logout(request)
    return redirect('register')
