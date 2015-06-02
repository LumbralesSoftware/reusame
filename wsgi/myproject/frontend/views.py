from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django import forms
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from services.models import Item

import json

class UserForm(forms.ModelForm):

    email = forms.CharField(max_length=75, required=True)

    class Meta:

        model = User
        fields = ('username', 'email')

class UserUpdate(UpdateView):
    model = User
    form_class = UserForm

    def get_object(self, queryset=None):
        return self.request.user

def home(request):
   context = RequestContext(request,
                           {'user': request.user})
   return render_to_response('index.html',
                             context_instance=context)

def request_item(request, id):
   data = json.loads(request.body)
   print data
   item = get_object_or_404(Item, pk=id)
   item.requestedBy(request.user, data['message'])
   return HttpResponse(json.dumps({"success": True}), content_type="application/json")
