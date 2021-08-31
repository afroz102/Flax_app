from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text

from users.models import UserProfile
from users.decorators import unauthenticated_user
from users.sendEmail import sendEmail
from users.utils import generate_token, validateRegisterForm
# from users.forms import CreateUserForm

# from django.contrib.auth.forms import UserCreationForm


@unauthenticated_user
def register_user(request):
    if request.method == 'GET':
        # form = CreateUserForm()
        context = {
            # 'form': form,
        }
        return render(request, 'auth/register.html', context)

    if request.method == 'POST':

        context = {'data': request.POST}

        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        validatePostForm = validateRegisterForm(request.POST)

        if validatePostForm['error']:
            messages.add_message(request, messages.ERROR,
                                 validatePostForm['msg'])

            return render(request, 'auth/register.html', context, status=400)

        # Create a new User
        newUser, created = User.objects.get_or_create(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        if created:
            newUser.set_password(password)
        newUser.is_active = False
        newUser.save()

        if created:
            UserProfile.objects.create(user=newUser)

        # Send registration email to user email
        sendEmail(request, newUser)

        messages.add_message(request, messages.SUCCESS,
                             'A link has been sent to your email.'
                             'click on the link to activate your account.')

        return redirect('login')


def activate_account(request, uidb64, token):
    try:
        # checking if the uid is same as user.id sent from the host
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except Exception as identifier:
        user = None

    # if id matches set user as verified and save
    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.add_message(request, messages.SUCCESS,
                             'account activated successfully')
        return redirect('login')

    # else return to activation failed page to show error message
    return render(request, 'auth/activate_failed.html', status=401)


@unauthenticated_user
def login_user(request):
    if request.method == "GET":
        return render(request, 'auth/login.html')

    if request.method == "POST":
        context = {
            'data': request.POST,
        }

        email = request.POST.get('email')
        password = request.POST.get('password')

        if email == '' or password == '':
            messages.add_message(request, messages.ERROR,
                                 'Please fill all the fields')
            return render(request, 'auth/login.html', status=401,
                          context=context)

        # user = authenticate(request, username=username, password=password)
        user = authenticate(request, username=email, password=password)
        # print("user: ", user)

        if not user:
            messages.add_message(request, messages.ERROR,
                                 'Email or Password is Wrong')
            return render(
                request,
                'auth/login.html',
                status=401,
                context=context
            )

        login(request, user)

        return redirect('home')


def logoutUser(request):
    logout(request)
    return redirect('login')
