from django.shortcuts import render, get_object_or_404, HttpResponse
from django.http import JsonResponse
from django.core import serializers

import json
from django.db.models import Q
from decouple import config

from django.core.mail import send_mail
from django.conf import settings

from info.forms import MessageForm
from info.models import (
    Project,
    Information,
    Message
)


def email_send(data):
    old_message = Message.objects.last()
    if old_message.name == data['name'] and old_message.email == data['email'] and old_message.message == data['message']:
        return False
    subject = 'Portfolio : Mail from {}'.format(data['name'])
    message = '{}\nSender Email: {}'.format(data['message'], data['email'])
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [settings.EMAIL_HOST_USER, ]
    send_mail(subject, message, email_from, recipient_list)
    return True


def homePage(request):
    template_name = 'homePage.html'
    context = {}

    if request.method == 'POST':
        if request.POST.get('rechaptcha', None):
            form = MessageForm(request.POST)
            if form.is_valid():
                form.save(commit=False)
                data = {
                    'name': request.POST['form-name'],
                    'email': request.POST['form-email'],
                    'message': request.POST['form-message']
                }
                if email_send(data):
                    form.save()

                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})
        return JsonResponse({'success': False, 'errors': "Oops, you have to check the recaptcha !"})

    if request.method == 'GET':
        form = MessageForm()
        projets = Project.objects.filter(show_in_slider=True).order_by('-id')
        info = Information.objects.first()
        context = {
            'info': info,
            'projets': projets,
            'form': form,
            'recaptcha_key': config("recaptcha_site_key", default="")
        }
    return render(request, template_name, context)


def projetsPage(request):
    template_name = 'projets/projets_page.html'
    if request.method == 'GET':
        projets = Project.objects.all().order_by('-id')
        context = {
            'projets': projets
        }
        return render(request, template_name, context)


def projectDetail(request, slug):
    template_name = 'projets/projet_detail.html'
    if request.method == 'GET':
        project = get_object_or_404(Project, slug=slug)
        return render(request, template_name, {'project': project})


def search(request):
    if request.method == 'POST':
        search_text = request.POST.get('searchText', False)
        if search_text:
            lookups = Q(title__icontains=search_text) | Q(
                description__icontains=search_text) | Q(tools__icontains=search_text)

            objs = Project.objects.filter(lookups)
            if objs:
                projets = Project.objects.filter(lookups).values()
                projets = list(projets)
                for project, obj in zip(projets, objs):
                    project.update({
                        'url': obj.get_project_absolute_url(),
                        'image_url': obj.image.url
                    })
                return JsonResponse({'success': True, 'projets': projets, 'searchText': search_text})
    return JsonResponse({'success': False, 'searchText': search_text})


def handler404(request, exception):
    return render(request, 'errors/404.html', status=404)


def test404(request):
    return render(request, 'errors/404.html')


