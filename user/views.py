from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User, UserUpdateForm


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User

    def get_object(self):
        return self.request.user


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm

    def get_object(self):
        return self.request.user
    
    def get_initial(self):
        user = self.request.user
        address = user.address
        split_address = address.split(',')
        street = split_address[0].lstrip()
        city = split_address[1].lstrip()
        post_code = split_address[2].lstrip()
        user = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone_num': user.phone_num,
            'street': street,
            'city': city,
            'post_code': post_code
        }

        return user
    
    def form_valid(self, form):
        form.instance.address = form.cleaned_data['address']
        name = form.cleaned_data['first_name']
        messages.success(self.request, 'Your details have been updated, ' + name)

        return super().form_valid(form)
