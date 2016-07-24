from django.conf.urls import url
from api import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^items/$', views.ItemList.as_view()),
    url(r'^items/(?P<pk>[0-9]+)/$', views.ItemDetail.as_view()),
    url(r'^components/$', views.ComponentList.as_view()),
    url(r'^components/(?P<pk>[0-9]+)/$', views.ComponentDetail.as_view()),
    url(r'^orders/$', views.OrderList.as_view()),
    url(r'^orders/(?P<pk>[0-9]+)/$', views.OrderDetail.as_view()),
    url(r'^itemhistory/$', views.ItemHistoryList.as_view()),
    url(r'^componenthistory/$', views.ComponentHistoryList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
