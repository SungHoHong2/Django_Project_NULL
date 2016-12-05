from django.shortcuts import redirect
from django.views.generic import TemplateView
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from member.dto.forms import LoginForm, RegisterForm, RegisterImageForm
from member.dto.serializer import LoginSerializer
from project_null.custom_authentication import CsrfExemptSessionAuthentication
from member.models import MyUser
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
import json
from collection.models import Image, Hash_Tag, Hash_Relationship
from rest_framework.response import Response
from django.db import connection
from rest_framework import status



class LoginPageView(TemplateView):
    template_name = 'base_dev/index.html'

    def get_context_data(self, **kwargs):
        context = super(LoginPageView, self).get_context_data(**kwargs)
        context['login_form'] = LoginForm()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        if request.user.is_authenticated:
            return redirect('member:around_me')
        else:
            return self.render_to_response(context)


class LoginActionView(viewsets.ModelViewSet):
    serializer_class = LoginSerializer

    # Login
    def create(self, request, *args, **kwargs):
        user = authenticate(username=request.data.get('username'), password=request.data.get('password'))
        if user is not None:
            auth_login(request, user)
        else:
            return Response({'error' : True})
        return Response({'success' : True})

    # logout
    def retrieve(self, request, *args, **kwargs):
        auth_logout(request)
        return redirect('/')


class RegisterPageView(TemplateView):
    template_name = 'base_dev/register.html'

    def get_context_data(self, **kwargs):
        context = super(RegisterPageView, self).get_context_data(**kwargs)
        context['register_form'] = RegisterForm()
        context['register_image_form'] = RegisterImageForm()
        return context


class RegisterActionView(viewsets.ModelViewSet):
    authentication_classes = (BasicAuthentication,CsrfExemptSessionAuthentication)

    def create(self, request, *args, **kwargs):

        myuser = MyUser.objects.create_user(
            username= request.data['username'],
            password = request.data['password_1'],
        )

        if request.data.get('image_file_ids') is not None:
            _index = 1
            for image_id in [x.strip() for x in request.data['image_file_ids'].split(',')]:
                img_obj = Image.objects.get(pk=image_id)
                img_obj.member = myuser
                img_obj.img_order = _index
                _index += 1
                img_obj.save()


        if request.data.get('hash_tag_names') is not None:
            hash_tag_names = request.data['hash_tag_names']
            print(hash_tag_names)

            _query_existing_hash_tags = (
                "select c.id, c.tag_name from collection_hash_tag c where c.tag_name in ( %s )"
            )

            with connection.cursor() as cursor:
                cursor.execute(_query_existing_hash_tags,[hash_tag_names])
                _hashtag_list = cursor.fetchall()
                _hashtag_list = [row[1] for row in _hashtag_list]

                for new_tag_name in [x.strip() for x in request.data['hash_tag_names'].split(',')]:
                    if new_tag_name not in _hashtag_list:
                        hash_tag = Hash_Tag.objects.create(tag_name= new_tag_name)
                    else:
                        hash_tag = Hash_Tag.objects.get(tag_name=new_tag_name)

                    Hash_Relationship.objects.create(member=myuser, hash_tag=hash_tag)

        auth_login(request, myuser)
        return Response({'response':True})


class NicknameDuplicate(viewsets.ModelViewSet):
    authentication_classes = (BasicAuthentication,CsrfExemptSessionAuthentication)

    def create(self, request, *args, **kwargs):
        my_users = MyUser.objects.filter(username=request.data.get('nickname'))

        if my_users.count() > 0 :
            return Response({'response':True})
        return Response({'response' : False })