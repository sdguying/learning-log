from django.shortcuts import render
from learning_logs.models import Topic, Entry
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    """定义learning_logs首页的视图"""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """定义所有主题的页面"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """显示单个主题内的详细条目"""
    topic = Topic.objects.get(id=topic_id)
    # 确认请求的主题属于当前用户
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """定义新增主题的form表单页面"""
    if request.method != 'POST':
        form = TopicForm()
    else:
        # 对post提交的数据进行处理
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """定义新增详细条目"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        form = EntryForm()
    else:
        # 对post提交的数据进行处理
        form = EntryForm(request.POST)
        if form.is_valid():
            # 检验post数据的有效性
            new_entry = form.save(commit=False)# 不保存在数据中，把数据实例化为new_entry
            new_entry.topic = topic # 将这些数据的主题属性设置为这个函数开头从Topic中获取的相应主题topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))

    context = {'topic':topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """编辑修改条目"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))

    context = {'form': form, 'topic': topic, 'entry': entry}
    return render(request, 'learning_logs/edit_entry.html', context)

@login_required
def edit_topic(request, topic_id):
    """编辑修改主题名称"""
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        form = TopicForm(instance=topic)
    else:
        form = TopicForm(instance=topic, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))

    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_topic.html', context)

