from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from django import forms
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import Avg
from django.utils.translation import ugettext as _

from services.models import Item, Category, UserRatings
from .search import *
from .images import *

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

class ItemForm(forms.ModelForm):
    category = forms.ModelChoiceField(
            queryset=Category.objects.all(),
            to_field_name="name",
            widget=forms.Select(attrs={'data-validation':'[NOTEMPTY]'}),
            label=_("Category")
    )

    class Meta:
        model = Item
        exclude=('created', 'owner', 'active', 'location')
        widgets = {
                'name': forms.TextInput(attrs={'data-validation':'[NOTEMPTY]'}),
                'description': forms.Textarea(attrs={'data-validation':'[NOTEMPTY]'}),
                'category': forms.TextInput(attrs={'data-validation':'[NOTEMPTY]'}),
                'image': forms.FileInput(attrs={'data-validation':'[NOTEMPTY]'}),
                'expires_on': forms.TextInput(attrs={'class':'datetimepicker', "placeholder": "yyyy-mm-dd --:--"}),
        }

class SearchItemsListView(ListView):
    model = Item
    template_name = "searchresults.html"

    def get_queryset(self):
        queryset = super(SearchItemsListView, self).get_queryset()
        # Get the q GET parameter
        if ('q' in self.request.GET) and self.request.GET['q'].strip():
            query_string = self.request.GET['q']
            search_fields=('name','description',)
            print query_string
            entry_query = get_query(query_string, search_fields)
            queryset = Item.objects.filter(entry_query).order_by('-id')
        # Return a filtered queryset
        return queryset.filter(active=True)

def home(request):
   context = RequestContext(
        request,
        {'item': ItemForm(), 'user': request.user}
   )
   return render_to_response('index.html', context_instance=context)

def vote_user(request, id):
   if not request.user.is_authenticated():
       return HttpResponseForbidden(json.dumps({"error":_('Please, log in first and try again.')}))

   item = get_object_or_404(Item, pk=id)
   vote, created = UserRatings.objects.get_or_create(
           voted_user=item.owner,
           voting_user =request.user,
           defaults={'punctuation': request.GET['punctuation']}
    )
   # if not created, update rating
   if not created:
        vote.punctuation = request.GET['punctuation']
        vote.save()

   #compute new average
   rating = UserRatings.objects.filter(voted_user=item.owner).aggregate(Avg('punctuation'))
   return HttpResponse(json.dumps({"rating": rating['punctuation__avg']}), content_type="application/json")

def request_item(request, id):
   if not request.user.is_authenticated():
      return HttpResponseForbidden(_('Please, log in first and try again.'))
   data = json.loads(request.body)
   item = get_object_or_404(Item, pk=id)
   item.requestedBy(request.user, data['message'])
   return HttpResponse(json.dumps({"success": True}), content_type="application/json")

def search(request):
   return HttpResponse(json.dumps({"success": True}), content_type="application/json")

def image_on_demand(request, id, width):
    if width in settings.ALLOWED_WIDTHS:
        #get item photo
        item = get_object_or_404(Item, pk=id)
        filetail = create_thumb(item, width)

        #image_data = Image.open(image_file)
        #response = HttpResponse(content_type="image/%s" % image_data.format) # create the proper HttpResponse object
        #try:
                #image_data.save(response, image_data.format, quality=90, optimize=1)
        #except:
                #image_data.save(response, image_data.format, quality=90)

        url = settings.MEDIA_URL + settings.IMAGE_ON_DEMAND_URL + width + '/' +  filetail
        #return response
        return HttpResponseRedirect('//' + request.get_host() + url)

