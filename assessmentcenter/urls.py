from django.conf.urls import url

from . import views

app_name = 'ac'

urlpatterns = [
    url(r'^$', views.OfferListView.as_view(), name='index'),
    url(r'^offers/list/$', views.OfferListView.as_view(), name='offer_list'),
    url(r'^offers/create/$', views.OfferCreateView.as_view(), name='offer_create'),
    url(r'^offers/(?P<pk>[0-9]+)/update/$', views.OfferUpdateView.as_view(), name='offer_update'),
    url(r'^offers/(?P<pk>[0-9]+)/delete/$', views.OfferDeleteView.as_view(), name='offer_delete'),
    url(r'^offers/(?P<pk>[0-9]+)/show/$', views.OfferDetailView.as_view(), name='offer_detail'),
    url(r'^benchmarks/list/$', views.BenchmarkListView.as_view(), name='benchmark_list'),
    url(r'^benchmarks/create/$', views.BenchmarkCreateView.as_view(), name='benchmark_create'),
    url(r'^benchmarks/(?P<pk>[0-9]+)/delete/$', views.BenchmarkDeleteView.as_view(), name='benchmark_delete'),
    url(r'^benchmarks/(?P<pk>[0-9]+)/update/$', views.BenchmarkUpdateView.as_view(), name='benchmark_update'),
    url(r'^benchmarks/(?P<pk>[0-9]+)/show/$', views.BenchmarkDetailView.as_view(), name='benchmark_detail'),
]
