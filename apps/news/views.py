from django.shortcuts import render
from django.http import HttpResponse
from .models import News,NewsCategory,Banner
from utils import restful
from django.conf import settings
from .serializers import NewsSerializer,CommentSerizlizer
from django.http import Http404
from .forms import PublicCommentForm
from .models import Comment
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from apps.xfzauth.decorators import xfz_login_required
# Create your views here.
def index(request):
    #每一页新闻数量
    count = settings.ONE_PAGE_NEWS_COUNT

    newses = News.objects.select_related('category','author').all()[0:count]
    categories = NewsCategory.objects.all()
    content = {
        'newses':newses,
        'categories':categories,
        'banners':Banner.objects.all(),
    }

    return render(request,'news/index.html',context = content)

def news_list(request):
    #/news/list/?p=2
    page = int(request.GET.get('p',1))
    # 0:不进行分类,直接按照时间倒序
    category_id = int(request.GET.get('category_id',0))

    start = (page-1)*settings.ONE_PAGE_NEWS_COUNT
    end = start + settings.ONE_PAGE_NEWS_COUNT

    if category_id == 0:
        newses = News.objects.select_related('category','author').all()[start:end]
    else:
        newses = News.objects.select_related('category','author').filter(category__id=category_id)[start:end]

    serializer = NewsSerializer(newses,many=True)
    data = serializer.data
    return restful.result(data=data)

def news_detail(request,news_id):
    try:
        news = News.objects.select_related('category', 'author').prefetch_related("comments__author").get(pk=news_id)
        context = {
            'news': news
        }
        return render(request, 'news/news_detail.html', context=context)
    except News.DoesNotExist:
        raise Http404

@xfz_login_required
def public_comment(request):
    form = PublicCommentForm(request.POST)
    if form.is_valid():
        news_id = form.cleaned_data.get('news_id')
        content = form.cleaned_data.get('content')
        news = News.objects.get(pk=news_id)
        comment = Comment.objects.create(content=content,news=news,author=request.user)
        serializer = CommentSerizlizer(comment)

        return restful.result(data=serializer.data)
    else:
        return restful.params_error(form.get_errors())

def search(request):
    q = request.GET.get('q')
    context = {}
    if q:
        newses = News.objects.filter(Q(title__icontains=q)|Q(desc__icontains=q)|Q(content__icontains=q))
        print("++++++++++++++++++++++++")
        print(newses)
        context['newses'] = newses
    return render(request,'search/search.html',context=context)

