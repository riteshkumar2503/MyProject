from django.conf.urls import url
from api_basic.views import article_list_view, modify_article_list_view, ArticleListApiView, ModifyArticleListApiView, ArticleListGenericApiView
from django.urls import path


# TEMPLATE TAGGING
app_name = 'api_basic_app123'

urlpatterns = [
    # url(r'^article/$', article_list_view, name='article_list_view_pattern_name'),
     path('articlefbv/', article_list_view, name='article_list_view_pattern_name'),
    path('articlecbv/', ArticleListApiView.as_view()),
    path('articlegenericview/', ArticleListGenericApiView.as_view()),

    # In earlier versions of Django, you had to use the url() method and pass a regular expressions with named capturing groups to capture URL parameters.     # In Django 2.0, you use the path() method with path converters to capture URL parameters.
    # url(r'^modify/(?P<pkxyz>[0-9]+)/$', modify_article_list_view, name='modify_article_list_view_pattern_name'),
    # path(r'modify/<int:pkxyz>/', modify_article_list_view, name='modify_article_list_view_pattern_name'),
    path(r'modify/<int:pkxyz>/', ModifyArticleListApiView.as_view(), name='modify_article_list_view_pattern_name'),

]
