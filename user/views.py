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
    
    def form_valid(self, form):
        name = form.cleaned_data['first_name']
        messages.success(self.request, 'Your details have been updated, ' + name)

        return super().form_valid(form)
