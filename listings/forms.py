from django import forms
from .models import Review

REVIEW_CHOICES = [(str(i), str(i)) for i in range(1, 6)]


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['text', 'rating']

        widget = {
            'text':
            forms.Textarea(attrs={
                'class': 'form-control shadow px-2',
                'rows': 6
            }),
            'rating': forms.RadioSelect
        }
