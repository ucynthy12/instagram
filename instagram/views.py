from django.shortcuts import render,redirect,get_object_or_404
from .forms import SignUpForm,PostForm,UpdateUserForm,CommentForm,UpdateUserProfileForm
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Post,Profile,Follow,Comment
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request,username = username,password = password)

            messages.success(request,'Account was created for ' + user)
        
            login(request,username)
             
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/registration_form.html', {'form': form})



@login_required(login_url='login')
def index(request):
    images = Post.objects.all()
    users = User.objects.exclude(id=request.user.id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user.profile
            post.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = PostForm()
    context= {
        'images': images,
        'form': form,
        'users': users,

    }
    return render(request, 'main/index.html', context)

@login_required(login_url='login')
def profile(request, username):
    images = request.user.profile.posts.all()
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(request.path_info)
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateUserProfileForm(instance=request.user.profile)
    
    return render(request, 'main/profile.html',{'user_form': user_form, 'profile_form': profile_form, 'images': images})

@login_required(login_url='login')
def user_profile(request, username):
    user_pro = get_object_or_404(User, username=username)
    if request.user == user_pro:
        return redirect('profile', username=request.user.username)
    user_posts = user_pro.profile.posts.all()
    
    followers = Follow.objects.filter(followed=user_pro.profile)
    follow_status = None
    for follower in followers:
        if request.user.profile == follower.follower:
            follow_status = True
        else:
            follow_status = False
    context = {
        'user_pro': user_pro,
        'user_posts': user_posts,
        'followers': followers,
        'follow_status': follow_status
    }
    print(followers)
    return render(request, 'main/user_profile.html', context)

@login_required(login_url='login')
def search_profiles(request):
    if 'search_user' in request.GET and request.GET['search_user']:
        name = request.GET.get("search_user")
        result = Profile.search_profile(name)
        print(result)
        message = f'name'
        return render(request, 'main/search.html',{'results': result,'message': message})
    else:
        message = "There's no profile name with that username "
    return render(request, 'main/search.html', {'message': message})


@login_required(login_url='login')
def unfollow(request, unfollowing):
    if request.method == 'GET':
        user_prof = Profile.objects.get(pk=unfollowing)
        unfollowed = Follow.objects.filter(follower=request.user.profile, followed=user_prof)
        unfollowed.delete()
        return redirect('user_profile', user_prof.user.username)


@login_required(login_url='login')
def follow(request, following):
    if request.method == 'GET':
        user_profs = Profile.objects.get(pk=following)
        follower = Follow(follower=request.user.profile, followed=user_profs)
        follower.save()
        return redirect('user_profile', user_profs.user.username)

def like_post(request,post_id):
    image = Post.objects.get(id=post_id)
    user = request.user
    image.likes.add(user)
    image.save()
    print(user)
    return redirect('comment',post_id)

   
   
@login_required(login_url='login')
def posting_comment(request, id):
    image = get_object_or_404(Post, pk=id)
    liked = False
    if image.likes.filter(id=request.user.id).exists():
        liked = True
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            savecomment = form.save(commit=False)
            savecomment.post = image
            savecomment.user = request.user.profile
            savecomment.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = CommentForm()
    return render(request, 'main/post.html',{ 'image': image,'form': form, 'liked': liked,'total_likes': image.total_likes()})
