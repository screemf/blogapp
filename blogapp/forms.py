from django import forms
from .models import Author,Post,Comment, Image

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'age', 'email', 'bio']

    def clean_age(self):
        age = self.cleaned_data['age']
        if age < 18:
            raise forms.ValidationError('Age must be greater than 18')
        return age

class ContactForm(forms.Form):
    name= forms.CharField(max_length=100)
    email= forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

    def clean_name(self):
        name = self.cleaned_data['name']
        if name == 'admin':
            raise forms.ValidationError('Name cannot be admin')
        return name


from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [ 'text']

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']