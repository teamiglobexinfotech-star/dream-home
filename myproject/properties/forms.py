from django import forms
from .models import Property
from .models import VisitSchedule
from .models import Project
from .models import BlogPost
from .models import BlogTag

# class ContactForm(forms.ModelForm):
#     class Meta:
#         model = ContactMessage
#         fields = ['full_name', 'mobile_number', 'email', 'subject', 'message']
#         widgets = {
#             'full_name': forms.TextInput(attrs={'placeholder': 'Enter your full name'}),
#             'mobile_number': forms.TextInput(attrs={'placeholder': 'Enter your mobile number'}),
#             'email': forms.EmailInput(attrs={'placeholder': 'Enter your email address'}),
#             'subject': forms.TextInput(attrs={'placeholder': 'Enter subject'}),
#             'message': forms.Textarea(attrs={'placeholder': 'Write your message here...', 'rows': 5}),
#         }

class ContactForm(forms.Form):

    full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={'placeholder': 'Enter your full name'}
        )
    )

    mobile_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(
            attrs={'placeholder': 'Enter your mobile number'}
        )
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'placeholder': 'Enter your email address'}
        )
    )

    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={'placeholder': 'Enter subject'}
        )
    )

    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Write your message here...',
                'rows': 5
            }
        )
    )
    

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        # Apne model ke field names check kar lein (jaise title, category, price etc.)
        fields = ['title', 'category', 'price', 'location', 'city', 'status', 'bedrooms', 'description', 'featured']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter property title'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'status': forms.Select(choices=[('Sale', 'Sale'), ('Rent', 'Rent')], attrs={'class': 'form-control'}),
            'bedrooms': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class VisitScheduleForm(forms.ModelForm):
    class Meta:
        model = VisitSchedule
        fields = ['property', 'name', 'email', 'phone', 'visit_date', 'message']
        widgets = {
            'property': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'placeholder': 'Enter your full name', 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter mobile number', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email address', 'class': 'form-control'}),
            'visit_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'message': forms.Textarea(attrs={'placeholder': 'Any specific requirement...', 'rows': 3, 'class': 'form-control'}),
        }



class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'title',
            'location',
            'description',
            'image',
            'category',
            'amenities',
            'status_text',
            'possession_or_completion',
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter project title'
            }),

            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter project location'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter project description'
            }),

            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),

            'category': forms.Select(attrs={
                'class': 'form-control'
            }),

            'amenities': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Club House, Gym, Parking'
            }),

            'status_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Under Construction'
            }),

            'possession_or_completion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. December 2027'
            }),
        }


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost

        fields = [
            'title',
            'category',
            'tags',
            'image',
            'excerpt',
            'content',
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter blog title'
            }),

            'category': forms.Select(attrs={
                'class': 'form-control'
            }),

            'tags': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'size': 5
            }),

            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),

            'excerpt': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter short blog excerpt'
            }),

            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Write your blog content here...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['tags'].queryset = BlogTag.objects.all().order_by('name')