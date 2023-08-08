from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models
from .form import ArticleForm
from django.db.models import Q

def main(request):
    return render(request,'news/main.html')

class NewsCreate(LoginRequiredMixin, CreateView):
    model = models.Article
    fields = '__all__'
    template_name = "news/article_form.html"

    def get(self, request): 
        form = ArticleForm()
        return render(request, 'news/article_form.html', {'form' : form})
    
    def post(self, request):
        form = ArticleForm(request.POST, request.FILES)
        print("request.FILES = ", request.FILES)
        print("request.POST = ", request.POST)
        if form.is_valid():
            news = form.save(commit=False)
        
            news.pub_date = form.cleaned_data['pub_date']
            news.headline = form.cleaned_data['headline']
            news.content = form.cleaned_data['content']
            news.reporter = form.cleaned_data['reporter']
            news.article_category = form.cleaned_data['article_category']

            if 'head_image' in request.FILES:
                news.head_image = request.FILES['head_image']

            if 'file_content' in request.FILES:
                news.file_content = request.FILES['file_content']

            news.save()
            return render(request, 'news/success.html')
    
        return render(request, 'news/article_form.html', {'form': form})

class NewsList(ListView):
    model = models.Article
    ordering = '-pub_date'
    

class NewsDetail(DetailView):
    model = models.Article


def kwd_search(request, *arg, **kwarg):
    category_list = []
    search_result = []
    and_kwd_list = []
    or_kwd_list = []

    if request.method == 'GET':
        d = dict(request.GET)
        category_list.extend(d['category'])
        print(category_list)
        kwd_list = request.GET['keyword'].split(' ')
        print(kwd_list)
        for kwd in kwd_list:
            if kwd.find('/') != -1:
                and_kwd_list.append(kwd.split('/'))
            else:
                or_kwd_list.append(kwd)

        or_kwd_list.extend(and_kwd_list)

        for category in category_list:
            all_querry = models.Article.objects.filter(article_category=category.upper())
            for s in or_kwd_list:
                search_result.extend(all_querry.filter(Q(reporter__full_name__icontains=s) | Q(headline__icontains=s) | Q(content__icontains=s)))
            print(search_result)
            tmp_querry = all_querry
            
            if len(and_kwd_list) > 0:
                print(and_kwd_list)
                for k in and_kwd_list:
                    tmp_query = all_querry
                    for s in k:
                        tmp_querry = tmp_querry.filter(Q(reporter__full_name__icontains=s) | Q(headline__icontains=s) | Q(content__icontains=s))
                    search_result.extend(tmp_querry)
        
        context={'category':category_list, 'kwd_list': kwd_list, 'article_list': search_result}
        print(search_result)
    return render (request, 'news/article_list.html', context)

def my_page(request, userid):
    user = models.Reporter.objects.get(rid=userid)
    print(user)

    my_page_list = models.Article.objects.filter(reporter__rid=user)
    context = {'article_list': my_page_list}
    return render(request, 'news/my_page_list.html', context)

def show_media(request, media):
    article_list =models.Article.objects.all()
    media_list = article_list.filter(article_category=media)
    print(media_list)
    context = {'media' : media, 'article_list' : media_list}
    return render(request, 'news/article_list.html', context)

def year_archive(request, year):
    year_article_list = models.Article.objects.filter(pub_date__year=year)
    print(year_article_list)
    context = {'year':year, 'article_list':year_article_list}
    return render(request, 'news/year_archive.html', context)


def month_archive(request, year, month):
    month_article_list = models.Article.objects.filter(pub_date__year=year, pub_date__month=month)
    context = {'year':year, 'month':month, 'article_list':month_article_list}
    return render(request, 'news/month_archive.html', context)


def article_detail(request, year, month, detail):
    detail_article_list = models.Article.objects.filter(pub_date__year=year, pub_date__month=month, pk=detail)
    context = {'year':year, 'month':month, 'detail':detail, 'article_list':detail_article_list}
    return(request, 'news/article_detail.html', context)
