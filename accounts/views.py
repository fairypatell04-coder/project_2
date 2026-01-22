from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CustomUserCreationForm, UserEditForm, ProfileEditForm

# -----------------------------
# Registration view
# -----------------------------
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()

            # Profile is already created by signals – just update it
            profile = user.profile
            profile.bio = form.cleaned_data.get('bio')
            profile.image = form.cleaned_data.get('image')
            profile.save()

            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('posts:feed')

    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


# -----------------------------
# Profile view
# -----------------------------
@login_required
def profile_view(request, username):
    user_obj = get_object_or_404(User, username=username)
    return render(request, 'posts/profile.html', {'user_obj': user_obj})


# -----------------------------
# Edit profile view
# -----------------------------
@login_required
def edit_profile(request, username):
    user_obj = get_object_or_404(User, username=username)
    if request.user != user_obj:
        return redirect('accounts:profile_view', username=request.user.username)

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=user_obj)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=user_obj.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile_view', username=user_obj.username)
    else:
        user_form = UserEditForm(instance=user_obj)
        profile_form = ProfileEditForm(instance=user_obj.profile)

    return render(request, 'accounts/profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'user_obj': user_obj
    })


# -----------------------------
# Home view
# -----------------------------
def home_view(request):
    return render(request, 'home.html')
