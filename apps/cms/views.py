from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST,require_GET
from django.views.generic import View
from apps.news.models import NewsCategory,News,Banner
from utils import restful
from .forms import EditNewsCategory,WriteNewsForm,AddBannerForm,EditBannerForm,EditNewsForm
import os
from django.conf import settings
from apps.news.serializers import BannerSerializer
from django.core.paginator import Paginator
from datetime import datetime
from django.utils.timezone import make_aware
from urllib import parse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
# Create your views here.

# 重定向
@staff_member_required(login_url='index')
def index(request):
    return render(request,'cms/index.html')
#使用装饰器,只有员工才能来到后台

@method_decorator(permission_required(perm='news.add_news',login_url='/'),name='dispatch')
class WriteNewsView(View):
    def get(self,request):
        categories = NewsCategory.objects.all()
        context = {
            'categories': categories,
        }
        return render(request, 'cms/write_news.html', context=context)
    def post(self,request):
        form = WriteNewsForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')
            category = NewsCategory.objects.get(pk=category_id)
            News.objects.create(title=title,desc=desc,thumbnail=thumbnail,content=content,category=category,author=request.user)
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())

@require_GET
@permission_required(perm='news.add_newscategory',login_url='/')
def news_category(request):
    categories = NewsCategory.objects.all()
    context = {
        'categories':categories,
    }
    return render(request,'cms/news_category.html',context=context)

@require_POST
@permission_required(perm='news.add_newscategory',login_url='/')
def add_news_category(request):
    name = request.POST.get('name')
    exists = NewsCategory.objects.filter(name=name).exists()
    if not exists:
        NewsCategory.objects.create(name=name)
        return restful.ok()
    else:
        return restful.params_error(message="分类已经存在")

@require_POST
@permission_required(perm='news.change_newscategory',login_url='/')
def edit_news_category(request):
    form = EditNewsCategory(require_POST)
    if form.is_valid():
        pk = form.cleaned_data.get('pk')
        name = form.cleaned_data.get('name')
        try:
            NewsCategory.objects.filter(pk=pk).update(name=name)
        except:
            return restful.params_error(message='pk不存在')
    else:
        return restful.params_error(message=form.get_error())

@require_POST
@permission_required(perm='news.delete_newscategory',login_url='/')
def delete_news_category(request):
    pk = request.POST.get('pk')
    try:
        NewsCategory.objects.filter(pk=pk).delete()
        return restful.ok()
    except:
        return restful.unauth(message='该分类不存在！')

@require_POST
@staff_member_required(login_url='index')
def upload_file(request):
    file = request.FILES.get('file')
    name = file.name
    with open(os.path.join(settings.MEDIA_ROOT,name),'wb') as fp:
        for chunk in file.chunks():
            fp.write(chunk)

    url = request.build_absolute_uri(settings.MEDIA_URL+name)
    return restful.result(data={'url':url})

@permission_required(perm='news.add_banner',login_url='/')
def banners(request):
    return render(request,'cms/banners.html')

@permission_required(perm='news.change_banner',login_url='/')
def banner_list(request):
    banners = Banner.objects.all()
    serialize = BannerSerializer(banners,many=True)
    return restful.result(data=serialize.data)

@permission_required(perm='news.add_banner',login_url='/')
def add_banner(request):
    form = AddBannerForm(request.POST)
    if form.is_valid():
        priority = form.cleaned_data.get('priority')
        image_url = form.cleaned_data.get('image_url')
        link_to = form.cleaned_data.get('link_to')
        banner = Banner.objects.create(priority=priority,image_url=image_url,link_to=link_to)
        return restful.result(data={"banner_id":banner.pk})
    else:
        return restful.params_error(message=form.get_errors())

@permission_required(perm='news.delete_banner',login_url='/')
def delete_banner(request):
    banner_id = request.POST.get('banner_id')
    Banner.objects.filter(pk=banner_id).delete()
    return restful.ok()

@permission_required(perm='news.change_banner',login_url='/')
def edit_banner(request):
    form = EditBannerForm(request.POST)
    if form.is_valid():
        pk = form.cleaned_data.get('pk')
        image_url = form.cleaned_data.get('image_url')
        link_to = form.cleaned_data.get('link_to')
        priority = form.cleaned_data.get('priority')
        Banner.objects.filter(pk=pk).update(image_url=image_url,link_to=link_to,priority=priority)
        return restful.ok()
    else:
        return restful.params_error(message=form.get_errors())

@method_decorator(permission_required(perm='news.change_news',login_url='/'),name='dispatch')
class NewsListView(View):
    def get(self,request):
        # request.GET：获取出来的所有数据，都是字符串类型
        page = int(request.GET.get('p',1))

        start = request.GET.get('start')
        end = request.GET.get('end')
        title = request.GET.get('title')
        # request.GET.get(参数,默认值)
        # 这个默认值是只有这个参数没有传递的时候才会使用
        # 如果传递了，但是是一个空的字符串，那么也不会使用默认值
        category_id = int(request.GET.get('category',0) or 0)

        newses = News.objects.select_related('category', 'author')

        if start or end:
            if start:
                start_date = datetime.strptime(start,'%Y/%m/%d')
            else:
                start_date = datetime(year=2019,month=1,day=1)
            if end:
                end_date = datetime.strptime(end,'%Y/%m/%d')
            else:
                end_date = datetime.today()
            newses = newses.filter(pub_time__range=(make_aware(start_date),make_aware(end_date)))

        if title:
            #大小写不敏感
            newses = newses.filter(title__icontains=title)

        if category_id:
            newses = newses.filter(category=category_id)
        #每一页显示多少文章
        paginator = Paginator(newses, 2)
        page_obj = paginator.page(page)

        context = {
            'categories': NewsCategory.objects.all(),
            #当前页的对象
            'newses': page_obj.object_list,
            'page_obj': page_obj,
            'paginator': paginator,
            'start': start,
            'end': end,
            'title': title,
            'category_id': category_id,
            # 有条件的翻页
            'url_query': '&'+parse.urlencode({
                'start': start or '',
                'end': end or '',
                'title': title or '',
                'category': category_id or ''
            })
        }

        context_data = self.get_pagination_data(paginator, page_obj)
        context.update(context_data)

        return render(request, 'cms/news_list.html', context=context)

    def get_pagination_data(self,paginator,page_obj,around_count=2):
        current_page = page_obj.number
        num_pages = paginator.num_pages

        left_has_more = False
        right_has_more = False

        if current_page <= around_count + 2:
            left_pages = range(1,current_page)
        else:
            left_has_more = True
            left_pages = range(current_page-around_count,current_page)

        if current_page >= num_pages - around_count - 1:
            right_pages = range(current_page+1,num_pages+1)
        else:
            right_has_more = True
            right_pages = range(current_page+1,current_page+around_count+1)

        return {
            # left_pages：代表的是当前这页的左边的页的页码
            'left_pages': left_pages,
            # right_pages：代表的是当前这页的右边的页的页码
            'right_pages': right_pages,
            'current_page': current_page,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'num_pages': num_pages
        }

@method_decorator(permission_required(perm='news.change_news',login_url='/'),name='dispatch')
class EditNewsView(View):
    def get(self,request):
        news_id = request.GET.get('news_id')
        news = News.objects.get(pk=news_id)
        context = {
            'news': news,
            'categories': NewsCategory.objects.all()
        }
        return render(request,'cms/write_news.html',context=context)

    def post(self,request):
        form = EditNewsForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')
            pk = form.cleaned_data.get("pk")
            category = NewsCategory.objects.get(pk=category_id)

            News.objects.filter(pk=pk).update(title=title,desc=desc,thumbnail=thumbnail,content=content,category=category)
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())

@require_POST
@permission_required(perm='news.delete_news',login_url='/')
def delete_news(request):
    news_id = request.POST.get('news_id')
    News.objects.filter(pk=news_id).delete()
    return restful.ok()