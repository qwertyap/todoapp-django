from django.forms import ModelForm
from .models import Todo, Image

class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'memo', 'important']


class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ['photo']
        labels = {'photo': ''}
