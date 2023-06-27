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
    essential_list = []
    kwd_list = []

    if request.method == 'GET':
        d = dict(request.GET)
        category_list.extend(d['category'])
        print(category_list)

        keyword = request.GET['keyword'].split(' ')

        for kwd in keyword:
            if '$' in kwd:
                kwd=kwd.replace('$','')
                essential_list.append(kwd)
            else:
                kwd_list.append(kwd)

        
        print(type(models.Article.objects.filter(Q(reporter__full_name__icontains=kwd_list))))
        
        for category in category_list:
            for kwd in range(len(kwd_list)):
                search_result.extend(models.Article.objects.filter((Q(reporter__full_name__icontains=essential_list[kwd]) | Q(headline__icontains=essential_list[kwd])) & (Q(reporter__full_name__icontains=kwd_list[kwd]) | Q(headline__icontains=kwd_list[kwd])), article_category=category.upper(),))

        context={'category':category_list, 'essential_list':essential_list, 'kwd_list': kwd_list, 'search_list': search_result}
        print(search_result)
    return render (request, 'news/show_search_result.html', context)


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
