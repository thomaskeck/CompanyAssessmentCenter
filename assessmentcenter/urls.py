from django.conf.urls import url

from . import views

app_name = 'ac'

urlpatterns = [
    url(r'^offers/$', views.OffersView.as_view(), name='offers'),
    url(r'^offers/add/$', views.OfferFormView.as_view(), name='offer_add'),
    url(r'^offers/(?P<pk>[0-9]+)/delete/$', views.offer_delete, name='offer_delete'),
    url(r'^offers/(?P<pk>[0-9]+)/show/$', views.OfferShowView.as_view(), name='offer_show'),
    url(r'^benchmarks/$', views.BenchmarksView.as_view(), name='benchmarks'),
    url(r'^benchmarks/(?P<pk>[0-9]+)/show/$', views.BenchmarkShowView.as_view(), name='benchmark_show'),
]
