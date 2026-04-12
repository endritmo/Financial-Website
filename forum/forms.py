from django import forms
from .models import Thread, Reply

class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['category', 'symbol', 'title', 'content']
        widgets = {
            'category': forms.Select(attrs={'class': 'search-input', 'style': 'width: 100%; margin-bottom: 1rem;'}),
            'symbol': forms.TextInput(attrs={'class': 'search-input', 'placeholder': 'e.g. BTCUSDT (Optional)', 'style': 'width: 100%; margin-bottom: 1rem;'}),
            'title': forms.TextInput(attrs={'class': 'search-input', 'placeholder': 'Thread Title', 'style': 'width: 100%; margin-bottom: 1rem;'}),
            'content': forms.Textarea(attrs={'class': 'search-input', 'placeholder': 'What are your thoughts on the market?', 'rows': 5, 'style': 'width: 100%; margin-bottom: 1rem;'}),
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'search-input', 'placeholder': 'Write your reply...', 'rows': 3, 'style': 'width: 100%; margin-bottom: 1rem;'}),
        }