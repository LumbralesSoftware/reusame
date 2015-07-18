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
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta

from services.models import Item, Category, UserRating, UserRequest
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
            queryset=Category.objects.all().order_by('name'),
            to_field_name="name",
            widget=forms.Select(attrs={'data-validation':'[NOTEMPTY]'}),
            label=_('Category name')
    )

    class Meta:
        model = Item
        exclude=('created', 'owner', 'active', 'location')
        widgets = {
                'name': forms.TextInput(attrs={'data-validation':'[NOTEMPTY]'}),
                'description': forms.Textarea(attrs={'rows': 3, 'data-validation':'[NOTEMPTY]', 'placeholder': _('For example: I am giving away this bike because I am not using it. It is in good working condition but might be a bit rusty.')}),
                'deal': forms.Textarea(attrs={'rows': 3, 'placeholder': _('I only ask you to give something away in this website and the item is yours.')}),
                'category': forms.TextInput(attrs={'data-validation':'[NOTEMPTY]'}),
                'image': forms.FileInput(attrs={'data-validation':'[NOTEMPTY]'}),
                'expires_on': forms.TextInput(attrs={'data-validation':'[NOTEMPTY]', 'class':'datetimepicker', "placeholder": "yyyy-mm-dd --:--"}),
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

    def get_context_data(self, **kwargs):
        context = super(SearchItemsListView, self).get_context_data(**kwargs)
        if 'q' in self.request.GET:
            context['q'] = self.request.GET['q']
        return context

def home(request):
   defaultExpiry= timezone.now() + timedelta(days=30)
   context = RequestContext(
        request,
        {
            'item': ItemForm(initial={'expires_on': defaultExpiry.strftime("%Y-%m-%d 00:00")}),
            'user': request.user,
            #'last_items': Item.objects.filter(active=True).order_by('-id')[:6][::-1]
            'last_items': Item.objects.filter(active=True).order_by('-category')[:6][::-1]

        }
   )
   return render_to_response('index.html', context_instance=context)

def vote_user(request, id):
   if not request.user.is_authenticated():
       return HttpResponseForbidden(json.dumps({"error": ugettext('Please, log in first and try again.')}))

   item = get_object_or_404(Item, pk=id)
   vote, created = UserRating.objects.get_or_create(
           voted_user=item.owner,
           voting_user =request.user,
           defaults={'punctuation': request.GET['punctuation']}
    )
   # if not created, update rating
   if not created:
        vote.punctuation = request.GET['punctuation']
        vote.save()

   #compute new average
   rating = UserRating.objects.filter(voted_user=item.owner).aggregate(Avg('punctuation'))
   return HttpResponse(json.dumps({"rating": rating['punctuation__avg']}), content_type="application/json")

@csrf_exempt
def request_item(request, id):
   if not request.user.is_authenticated():
       return HttpResponseForbidden(json.dumps({"success": False, "error": ugettext('Please, log in first and try again.')}))
   data = json.loads(request.body)
   item = get_object_or_404(Item, pk=id)
   #item.requestedBy(request.user, data['message'])

   itemRequest, created = UserRequest.objects.get_or_create(
           requester=request.user,
           item=item,
           defaults={'message': data['message']}
   )

   # if already requested, do nothing
   if created:
       itemRequest.request()
       itemRequest.save()

   return HttpResponse(json.dumps({"success": True}), content_type="application/json")

def search(request):
   return HttpResponse(json.dumps({"success": True}), content_type="application/json")

def image_on_demand(request, shape, id, width):
    if width in settings.ALLOWED_WIDTHS:
        #get item photo
        item = get_object_or_404(Item, pk=id)
        filetail = create_thumb(item.image, shape, width)

        #image_data = Image.open(image_file)
        #response = HttpResponse(content_type="image/%s" % image_data.format) # create the proper HttpResponse object
        #try:
                #image_data.save(response, image_data.format, quality=90, optimize=1)
        #except:
                #image_data.save(response, image_data.format, quality=90)

        url = settings.MEDIA_URL + settings.IMAGE_ON_DEMAND_URL + shape + '/' + width + '/' +  filetail
        #return response
        return HttpResponseRedirect('//' + request.get_host() + url)

