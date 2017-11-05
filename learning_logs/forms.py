from django import forms
from .models import Topic, Entry

class TopicForm(forms.ModelForm):
    """主题表单"""
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}

class EntryForm(forms.ModelForm):
    """新增条目"""
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
