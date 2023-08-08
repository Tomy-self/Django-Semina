from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.NewsList.as_view(), name="list"),
    path('kwd_search/',views.kwd_search),
    path('news/<int:pk>/', views.NewsDetail.as_view(), name='detail'),
    path('create/', views.NewsCreate.as_view(), name='create'),
    path('articles/<int:year>/', views.year_archive),
    path('articles/<int:year>/<int:month>/', views.month_archive),
    path('articles/<int:year>/<int:month>/<int:pk>/', views.article_detail),
    path('show_media/<str:media>/', views.show_media),
    path('mypage/<str:userid>', views.my_page),
]

