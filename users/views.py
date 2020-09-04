from django.urls import reverse
from django.views.generic import ListView, TemplateView, DetailView, UpdateView
from django.utils.translation import gettext as _
from django.http import Http404, HttpResponseRedirect
from django.core.paginator import InvalidPage

from rest_framework import viewsets

from .forms import UserForm, HomeForm, imageformset
from .serializers import UserSerializer, HomeSerializer
from .models import User, Home


class HomeView(TemplateView, ListView):
    template_name = 'users/home.html'
    model = User
    queryset = User.objects.all()
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        self.object_list = User.objects.all()
        user_queryset = User.objects.all()
        homes_queryset = Home.objects.all()
        page_size = self.paginate_by
        user_paginator, user_page, user_queryset, user_is_paginated = self.paginate_queryset(user_queryset, page_size, "user_page")
        home_paginator, home_page, home_queryset, home_is_paginated = self.paginate_queryset(homes_queryset, page_size, "home_page")
        context = {
            'user_paginator': user_paginator,
            'user_page': user_page,
            'user_is_paginated': user_is_paginated,
            'user_queryset': user_queryset,
            'home_paginator': home_paginator,
            'home_page': home_page,
            'home_is_paginated': home_is_paginated,
            'home_queryset': home_queryset
        }

        context.update(kwargs)
        return context

    def paginate_queryset(self, queryset, page_size, page_kwarg):
        """Paginate the queryset, if needed."""
        paginator = self.get_paginator(
            queryset, page_size, orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty())
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
        try:
            page_number = int(page)
        except ValueError:
            if page == 'last':
                page_number = paginator.num_pages
            else:
                raise Http404(_('Page is not “last”, nor can it be converted to an int.'))
        try:
            page = paginator.page(page_number)
            return (paginator, page, page.object_list, page.has_other_pages())
        except InvalidPage as e:
            raise Http404(_('Invalid page (%(page_number)s): %(message)s') % {
                'page_number': page_number,
                'message': str(e)
            })


class UserViewSet(viewsets.ModelViewSet):
    model = User
    serializer_class = UserSerializer
    queryset = User.objects.all()
    allowed_methods = "GET", "POST", "PATCH", "DELETE"


class HomeViewSet(viewsets.ModelViewSet):
    model = Home
    serializer_class = HomeSerializer
    queryset = Home.objects.all()
    allowed_methods = "GET", "POST", "PATCH", "DELETE"


class UserView(ListView):
    model = User
    paginate_by = 10
    template_name = 'users/users_list.html'
    queryset = User.objects.all()


class UserDetailView(DetailView):
    model = User
    slug_field = 'id'


class UserUpdateView(UpdateView):
    model = User
    slug_field = 'id'
    form_class = UserForm


class HomeUpdateView(UpdateView):
    model = Home
    slug_field = 'id'
    form_class = HomeForm

    def get_success_url(self):
        self.success_url = reverse('homes-update', args=(self.object.id,))
        return self.success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['img_form'] = imageformset(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['img_form'] = imageformset(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        home_form = self.get_form(form_class)
        img_form = imageformset(self.request.POST, self.request.FILES, instance=self.object)

        if (home_form.is_valid() and img_form.is_valid()):
            return self.form_valid(home_form, img_form)
        else:
            return self.form_invalid(home_form, img_form)

    def form_valid(self, home_form, img_form):
        self.object = home_form.save()
        img_form.instance = self.object
        img_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, home_form, img_form):
        return self.render_to_response(self.get_context_data(home_form=home_form,
                                                             img_form=img_form))


class HomesView(ListView):
    model = Home
    paginate_by = 10
    template_name = 'users/homes_list.html'
    queryset = Home.objects.all()

    def get_queryset(self):
        user_id = self.request.GET.get("user_id")
        queryset = super().get_queryset().filter()
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset


