from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django import forms
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import Avg

from services.models import Item, Category, UserRatings

from PIL import Image, ImageOps, ImageDraw

import json
import os

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
    category = forms.ModelChoiceField(queryset=Category.objects.all(), to_field_name="name",widget=forms.Select(attrs={'data-validation':'[NOTEMPTY]'}))

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

def home(request):
   context = RequestContext(
        request,
        {'item': ItemForm(), 'user': request.user}
   )
   return render_to_response('index.html', context_instance=context)

def vote_user(request, id):
   if not request.user.is_authenticated():
      return HttpResponseForbidden('Please, log in first and try again.')
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
      return HttpResponseForbidden('Please, log in first and try again.')
   data = json.loads(request.body)
   item = get_object_or_404(Item, pk=id)
   item.requestedBy(request.user, data['message'])
   return HttpResponse(json.dumps({"success": True}), content_type="application/json")

def image_on_demand(request, id, width):

    if width in settings.ALLOWED_WIDTHS:
        #get item photo
        item = get_object_or_404(Item, pk=id)

        #path to original image and file split
        original_file = os.path.join(settings.MEDIA_ROOT, item.image.name)
        filehead, filetail = os.path.split(original_file)

        #check if image path exists otherwise create it
        image_path = os.path.join(settings.IMAGE_ON_DEMAND_DIR, width)
        if not os.path.exists(image_path):
            os.mkdir(image_path)

        #create image path. note, width SHOULD be a string otherwise os.path.join fails
        image_file = os.path.join(settings.IMAGE_ON_DEMAND_DIR, width, filetail)

        # we need te calculate the new height based on the ratio of the original image, create integers
        ratio = float(float(item.image.width) / float(item.image.height))
        height = int(float(width) / ratio)
        iwidth = int(width)


        # check if file exists and the original file hasn't updated in between
        if os.path.exists(image_file) and os.path.getmtime(original_file) > os.path.getmtime(image_file):
                os.unlink(image_file)

        # if the image wasn't already resized, resize it.Maybe I should rewrite it to do this directly with PythonMagick
        # taken from snippet http://www.djangosnippets.org/snippets/453/

        if not os.path.exists(image_file):
            image = Image.open(original_file)
            #assert False
            image.thumbnail([iwidth, height], Image.ANTIALIAS)
            format = 'png' # conver to PNG to be able to set the transparent mask

            bigsize = (image.size[0] * 3, image.size[1] * 3)
            mask = Image.new('L', bigsize, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + bigsize, fill=255)
            mask = mask.resize(image.size, Image.ANTIALIAS)
            image.putalpha(mask)

            #optional unsharp mask using snippet http://www.djangosnippets.org/snippets/1267/
            #image = usm(image,settings.RADIUS,settings.SIGMA,settings.AMOUNT,settings.THRESHOLD)

            try:
                image.save(image_file, format, quality=90, optimize=1)
            except:
                image.save(image_file, format, quality=90)


        #image_data = Image.open(image_file)
        #response = HttpResponse(content_type="image/%s" % image_data.format) # create the proper HttpResponse object

        #try:
                #image_data.save(response, image_data.format, quality=90, optimize=1)
        #except:
                #image_data.save(response, image_data.format, quality=90)

        url = settings.MEDIA_URL + settings.IMAGE_ON_DEMAND_URL + width + '/' +  filetail
        #return response
        return HttpResponseRedirect('//' + request.get_host() + url)

