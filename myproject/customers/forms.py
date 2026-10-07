from django import forms
from django.contrib.auth import get_user_model
from properties.models import Property
from properties.models import Property, Enquiry


User = get_user_model()

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['full_name', 'mobile_number', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

class LoginForm(forms.Form):
    username_or_mobile = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)
    remember_me = forms.BooleanField(required=False)

#Property Form 

# class PropertyForm(forms.ModelForm):
#     class Meta:
#         model = Property
        
#         fields = [
#             'title', 
#             'description', 
#             'category', 
#             'status', 
#             'price', 
#             'location', 
#             'city', 
#             'bedrooms', 
#             'bathrooms', 
#             'area', 
#             'featured', 
#             'image'
#         ]



class PropertyForm(forms.ModelForm):

    # Custom image field
    # Actual multiple files hum view me
    # request.FILES.getlist('images') se handle karenge.
    images = forms.FileField(
        required=False,
        label='Property Images',
        widget=forms.FileInput(
            attrs={
                'accept': 'image/*',
                'id': 'property-images-input'
            }
        )
    )

    class Meta:
        model = Property

        fields = [
            'title',
            'description',
            'category',
            'status',
            'price',
            'location',
            'city',
            'bedrooms',
            'bathrooms',
            'area',
            'featured',
        ]




#(Dashboard se Lead / Enquiry add karne ke liye)
class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = [ 'name', 'email', 'phone', 'property_type', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter full name', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email address', 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter mobile number', 'class': 'form-control'}),
            'property_type': forms.TextInput(attrs={'placeholder': 'e.g. 2 BHK Apartment', 'class': 'form-control'}),
            
            'message': forms.Textarea(attrs={'placeholder': 'Write your message...', 'rows': 4, 'class': 'form-control'}),
        }

