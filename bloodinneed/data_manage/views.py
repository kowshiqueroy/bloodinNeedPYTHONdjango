from django.contrib.auth import authenticate, logout,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

# Create your views here.

from django.shortcuts import render
from django.views.generic import DetailView

from .forms import DonorCreationForm, UserAuthenticationForm, BlogForm,  DonorFindForm
from .models import Donor, Blog


def home(request):
    if request.user.is_authenticated:
        return redirect('profile', pk=request.user.id)
    else:
        return render(request, 'data_manage/home.html')

def blog(request):

   context={}

   blogs = Blog.objects.all().order_by('-date')
   context['blogs']= blogs


   return render(request, 'data_manage/blog.html',context=context)

@login_required
def donor_list(request):

   context={}

   donor_list = Donor.objects.filter(is_donor=True).order_by('blood_group')
   context['donor_list']= donor_list
   donor_find = DonorFindForm(request.POST)
   context['form']= donor_find


   if request.method=="POST":

       if donor_find.is_valid():
           donor_find = donor_find.save(commit=False)
           choice=request.POST['find']
           donor_list = Donor.objects.filter(blood_group=choice).order_by('full_name')
           context['donor_list']=donor_list
           if not choice:
               donor_list = Donor.objects.all().order_by('blood_group')
               context['donor_list'] = donor_list

           return render(request, 'data_manage/donor_list.html',context=context)





   return render(request, 'data_manage/donor_list.html',context=context)





def profile(request):
   if request.user.is_authenticated:
       context = {}
       blog_blood = Blog.objects.filter(blog_blood_group=request.user.blood_group).order_by('-date')
       context['blog_blood'] = blog_blood
       print("blog_blood")
       return render(request, 'data_manage/profile.html',context=context)
   else:
    return redirect('signup', pk=request.user.id)

@login_required
def post(request):

   context={}
   if request.method == 'POST':
      blogform=BlogForm(request.POST, request.FILES)

      if blogform.is_valid():
         blognew=blogform.save(commit=False)
         blognew.user = request.user
         blognew.save()
         return redirect('blog')
      else:
         context['form'] = blogform
   else:  # GET request
      blogform = BlogForm()

      context['form'] =blogform

   return render(request, 'data_manage/post.html', context=context)


def signup(request):
   # go to profile
   # if already logged in
   if request.user.is_authenticated:
      return redirect('profile', pk=request.user.id)

   context = {}

   if request.method == 'POST':
      donorcreationform = DonorCreationForm(request.POST, request.FILES)

      if donorcreationform.is_valid():
         donor = donorcreationform.save()

         username = donorcreationform.cleaned_data.get('username')
         raw_password = donorcreationform.cleaned_data.get('password1')

         authenticated_account = authenticate(username=username, password=raw_password)
         login(request, authenticated_account)

         return redirect('profile', pk=donor.id)
      else:
         context['form'] = donorcreationform

   else:  # GET request
      donorcreationform = DonorCreationForm()

      context['form'] = donorcreationform

   return render(request, 'data_manage/signup.html', context=context)


def login_view(request):
   if request.user.is_authenticated:
      return redirect('profile', request.user.id)

   context = {}

   # initialize authentication form
   # to avoid UnboundLocalError
   # due to not assigning it
   form = None
   if request.method == 'POST':
      form = UserAuthenticationForm(request.POST)
      if form.is_valid():
         username = request.POST['username']
         password = request.POST['password']
         user = authenticate(username=username, password=password)

         if user:
            login(request, user)
            return redirect('profile', pk=user.id)

   else:
      form = UserAuthenticationForm()

   context['form'] = form

   return render(request, 'data_manage/login.html', context)






@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

class UserDetailView(LoginRequiredMixin, DetailView):
    model = Donor
    template_name = 'data_manage/profile.html'

    def get(self, request, pk):
        context = {}

        user = Donor.objects.get(id=pk)

        # only display the update button
        # if a user is view their own profile
        display_btn_update = False
        if request.user == user:
            display_btn_update = True

        context['user'] = user
        context['display_btn_update'] = display_btn_update

        context = {}
        blog_blood = Blog.objects.filter(blog_blood_group=request.user.blood_group).order_by('-date')
        context['blog_blood'] = blog_blood
        print("blog_blood")

        return render(request, self.template_name, context=context)

@login_required
def update(request):
    context = {}

    user = request.user

    if request.method == 'POST':
        form = DonorCreationForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            Donor = form.save()

            return redirect('login')
        else:
            context['form'] = form

    else: # GET request
        form = DonorCreationForm(instance=user)

        context['form'] = form

    return render(request, 'data_manage/update.html', context=context)








