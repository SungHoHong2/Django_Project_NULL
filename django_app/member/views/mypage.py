from django.shortcuts import redirect
from django.views.generic import TemplateView
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from member.dto.forms import LoginForm, RegisterForm, RegisterImageForm
from project_null.custom_authentication import CsrfExemptSessionAuthentication
from member.models import MyUser, Like_Relationship
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
import json
from collection.models import Image, Hash_Tag, Hash_Relationship
from django.db import connection
from rest_framework.response import Response
from collection.serializer import ImageSerializer
from django.conf import settings

class MyPageProfileView(TemplateView):
    template_name = 'base_test/my_page/profile.html'

    def get_context_data(self, **kwargs):
        context = super(MyPageProfileView, self).get_context_data(**kwargs)
        return context
