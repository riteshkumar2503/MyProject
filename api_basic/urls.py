from django.conf.urls import url
from api_basic.views import function_based_view, function_based_view2,ClassBasedView, ClassBasedView2, GenericView, ArticleViewSet, ArticleGenericViewSet, ArticleModelViewSet
from django.urls import path
from django.conf.urls import url, include


from rest_framework.routers import DefaultRouter
router_x = DefaultRouter()
router_x.register('articleviewsettt', ArticleViewSet, basename='article101')
router_x.register('articlegenericviewsettt', ArticleGenericViewSet, basename='article102')
router_x.register('articlemodelviewsettt', ArticleModelViewSet, basename='article103')


urlpatterns = router_x.urls


# TEMPLATE TAGGING
app_name = 'api_basic_app123'

urlpatterns = [
    path('api2/', include(router_x.urls)),
    path('articlefbv/', function_based_view, name='function_based_view_pattern_name'),
    # url(r'^modify/(?P<pkxyz>[0-9]+)/$', function_based_view2, name='function_based_view2_pattern_name'),  In earlier versions of Django, you had to use the url() method and pass a regular expressions with named capturing groups to capture URL parameters.     # In Django 2.0, you use the path() method with path converters to capture URL parameters.
    path(r'articlefbv2/<int:pkxyz>/', function_based_view2, name='function_based_view2_pattern_name'),

    path('articlecbv/', ClassBasedView.as_view()),
    path(r'articlecbv2/<int:pkxyz>/', ClassBasedView2.as_view(), name='class_based_view2_pattern_name'),

    path(r'articlegenericview/<int:id>/', GenericView.as_view(), name='generic_view_pattern_name'),

]
