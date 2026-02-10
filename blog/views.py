from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,Http404
from django.urls import reverse
from .models import Post,AboutUs,Category
from django.core.paginator import Paginator
from .forms import ContactForm,RegisterForm,LoginForm,ForgotPasswordForm,ResetPasswordForm,PostForm
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.models import User,Group
from django.contrib.auth.decorators import login_required,permission_required

def index(request):
    blog_title = "Latest Posts"
    posts = Post.objects.filter(is_published=True)

    # Paginator
    paginator = Paginator(posts, 5)  # Show 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request,'index.html',{'title':blog_title, 'page_obj': page_obj})

def detail(request,id):

    if request.user and not request.user.has_perm('blog.view_post'):
        messages.error(request,"You have No permission to view any posts.")
        return redirect('index')

    try:
        posts = Post.objects.get(pk=id)
        related_posts = Post.objects.filter(category=posts.category).exclude(pk=id)
    
    except Post.DoesNotExist:
        raise Http404("Post doesn't exist.")

    return render(request,'detail.html',{'post':posts, 'related_posts': related_posts})


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if form.is_valid():
            # send email
            success_message = "your Email has been sent!"
            return render(request,'contact.html',{'form':form,'success_message':success_message})
        
        return render(request,'contact.html',{'form':form,'name':name,'email':email,'message':message})
    return render(request, 'contact.html')

def about_view(request):
    about_content = AboutUs.objects.first()
    if about_content is None or not about_content.content:
        about_content='Default Content shows Here' #Default
    else:
        about_content = about_content.content
    return render(request,'about.html',{'about_content':about_content})

def register(request):
    form  = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            reader_groups,created = Group.objects.get_or_create(name="Readers")
            user.groups.add(reader_groups)
            # print("Register Success!")
            messages.success(request,"Registration Successfull🎉, You can Login.")
            return redirect("login")
        
    return render(request,'register.html',{'form':form})

def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username,password=password)
            if user is not None:
                auth_login(request,user)
                print("Login Success!")
                return redirect("dashboard")

                
    return render(request,'login.html',{'form':form})


def dashboard(request):
    blog_title = "My Posts"
    all_posts = Post.objects.filter(user=request.user)
    # Paginator
    paginator = Paginator(all_posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request,'dashboard.html',{'blog_title': blog_title,'page_obj' :page_obj})


def logout(request):
    auth_logout(request)
    return redirect('index')


def forgot_password(request):
    form = ForgotPasswordForm()
    if request.method=='POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)

            # send email to reset password
            token = default_token_generator.make_token(user)
            # uid = urlsafe_base64_encode(force_bytes(user))
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            current_site = get_current_site(request)
            domain = current_site.domain
            subject = "Reset Password Requested"
            message = render_to_string('reset_password_email.html',{
                'domain':domain,
                'uid':uid,
                'token':token,
            })

            send_mail(subject,message,'noreply@example.com',[email])
            messages.success(request,'Email has been sent.')


    return render(request,'forgot_password.html',{'form':form})


def reset_password(request,uidb64,token):
    form = ResetPasswordForm()
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            try:
                uid = urlsafe_base64_decode(uidb64).decode()
                user = User.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None
            if user is not None and default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                messages.success(request,'Password has been reset successfully. You can login now.')
                return redirect('login')
            else:
                messages.error(request,'This link is invalid or has expired.')

    return render(request,'reset_password.html',{'form':form})


@login_required
@permission_required('blog.add_post',raise_exception=True)
def new_post(request):
    categories = Category.objects.all()
    form = PostForm()
    if request.method =='POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('dashboard')
    return render(request,'new_post.html',{'categories':categories, 'form':form})


@login_required
@permission_required('blog.change_post',raise_exception=True)

def edit_post(request,post_id):
    categories = Category.objects.all()
    post = get_object_or_404(Post,id=post_id)
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request,'Post Updated Successfully🎉.')
            return redirect('dashboard')
    return render(request,'edit_post.html',{'categories':categories,'post':post,'form':form})


@login_required
@permission_required('blog.delete_post',raise_exception=True)
def delete_post(request,post_id):
    post = get_object_or_404(Post,id=post_id)
    post.delete()
    messages.success(request,'Post Deleted Successfully!')
    return redirect('dashboard')


@login_required
@permission_required('blog.can_publish_post',raise_exception=True)

def publish_post(request,post_id):
    post = get_object_or_404(Post,id=post_id)
    post.is_published = True
    post.save()
    messages.success(request,'Post published Successfully🎉')
    return redirect('dashboard')
