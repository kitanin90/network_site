from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic import CreateView, TemplateView, ListView, UpdateView, DeleteView

from blog.forms import RegisterForm, EditProfileForm, LoginForm, CreateGroupForm, EditCommunityForm
from blog.models import Account, Community
from blog.models import Contact, ConnectCommunityPeople


class CreateGroup(CreateView):
    model = Community
    form_class = CreateGroupForm
    template_name = 'blog/creategroup.html'
    success_url = '/panel/group'

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.save()
        return HttpResponseRedirect(self.success_url)


class HomeView(TemplateView):
    template_name = 'blog/index.html'


class Registration(CreateView):
    model = Account
    form_class = RegisterForm
    template_name = 'blog/registration.html'
    success_url = '/panel/workflow'

    def form_valid(self, form):
        form.save()
        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return HttpResponseRedirect(self.success_url)


class UpdateProfile(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = Account
    template_name = 'blog/edit_profile.html'
    context_object_name = 'account'
    form_class = EditProfileForm
    slug_url_kwarg = 'username'
    success_url = '/panel/workflow/'

    def get_object(self, queryset=None):
        obj = get_object_or_404(Account, pk=self.request.user.id)
        return obj


class UpdateGroup(LoginRequiredMixin, UpdateView, Community):
    login_url = '/login/'
    model = Community
    template_name = 'blog/edit_group.html'
    context_object_name = 'community'
    form_class = EditCommunityForm
    slug_url_kwarg = 'name'
    success_url = '/panel/group/'

    def get_object(self, queryset=None):
        obj = Community.objects.filter(id=self.kwargs.get("pk")).first()
        return obj


class GroupDelete(LoginRequiredMixin, DeleteView):
    model = Community
    success_url = '/panel/group/'

    def get_object(self, queryset=None):
        obj = super(GroupDelete, self).get_object()
        if not obj.creator == self.request.user:
            return HttpResponseRedirect(self.success_url)
        return obj


class AccountLoginView(LoginView):
    template_name = 'blog/login.html'
    form_class = LoginForm


class UserWorkflow(LoginRequiredMixin, ListView):
    login_url = '/panel/login'
    model = Account
    template_name = 'blog/workflow.html'
    context_object_name = 'account'

    def get_queryset(self):
        return Account.objects.get(username=self.request.user)


@login_required
def group(request):
    if request.method == 'GET':
        follow_group = ConnectCommunityPeople.objects.filter(users=request.user.id)
        my_groups = Community.objects.filter(creator=request.user.id)
        all_groups = Community.objects.all()
        return render(request,
                      'blog/group.html',
                      {'my_groups': my_groups,
                       'follow_group': follow_group,
                       'all_groups': all_groups,
                       })


@login_required
def user_list(request):

    if request.method == 'GET':
        follow_users = Contact.objects.filter(user_from=request.user.id)

        # .exclude(username=request.user.username) удаляем из списка всех юзеров
        # текущего залогиненого юзера
        users = Account.objects.all().exclude(
            username=request.user.username).exclude(
            username__in=[u.user_to.username for u in follow_users])
        # 2 exclude удаляет из списка уже подписаных юзеров

        return render(request,
                      'blog/list.html',
                      {'users': users,
                       'follow_users': follow_users})


@login_required
def user_detail(request, username):
    user_id = request.user.pk
    success_url = '/panel/users/'

    if request.method == 'GET':
        user = get_object_or_404(Account, username=username)
        return render(request,
                      'blog/detail.html',
                      {'user': user})

    if request.method == 'POST':
        user = Account.objects.get(username=username)
        if not Contact.objects.filter(user_from=request.user, user_to=user):
            Contact.objects.get_or_create(user_from=request.user, user_to=user)
            Contact.objects.get_or_create(user_from=user, user_to=request.user)
        else:
            Contact.objects.filter(user_from=request.user, user_to=user).delete()
            Contact.objects.filter(user_from=user, user_to=request.user).delete()

        return HttpResponseRedirect(success_url)
    return JsonResponse({'status': 'ok'})


@login_required
def group_detail(request, name):
    success_url = '/panel/group'

    if request.method == 'GET':
        community = get_object_or_404(Community, name=name)

        group_users = [e.users for e in ConnectCommunityPeople.objects.filter(
            group__id=Community.objects.filter(name=name)[0].id)]

        return render(request,
                      'blog/detail_group.html',
                      {'community': community,
                       'group_users': group_users,
                       })

    if request.method == 'POST':
        community = Community.objects.get(name=name)
        if not ConnectCommunityPeople.objects.filter(users=request.user, group=community):
            ConnectCommunityPeople.objects.get_or_create(users=request.user, group=community)
        else:
            ConnectCommunityPeople.objects.filter(users=request.user, group=community).delete()

        return HttpResponseRedirect(success_url)

    return JsonResponse({'status': 'ok'})
