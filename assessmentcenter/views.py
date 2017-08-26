import datetime

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic, View
from django.db.models import Count, Avg

from django.utils.dateparse import parse_datetime
from django import forms

from .models import Benchmark, Offer, Rating


class OffersView(generic.ListView):
    def get_queryset(self):
        return Offer.objects.order_by('deadline').annotate(Avg('rating__rating'))


class BenchmarksView(generic.ListView):
    def get_queryset(self):
        return Benchmark.objects.order_by('weight')


class OfferShowView(generic.DetailView):
    model = Offer
    

def offer_delete(request, pk):
    offer = Offer.objects.get(pk=pk)
    offer.delete()
    return HttpResponseRedirect(reverse('ac:offers'))


class BenchmarkShowView(generic.DetailView):
    model = Benchmark


class OfferForm(forms.Form):
    name = forms.CharField(label='Offer Name', min_length=1, max_length=100, strip=True, required=True)
    description = forms.CharField(label='Offer Description', max_length=10000, widget=forms.Textarea)
    deadline = forms.DateField(label='Deadline', required=True,
                               widget=forms.DateInput(attrs={'type':'date'}))

    def __init__(self, *args, **kwargs):
        super(OfferForm, self).__init__(*args, **kwargs)
        self.benchmarks = Benchmark.objects.order_by('weight')
        for benchmark in self.benchmarks:
            self.fields['bm_%s' %benchmark.id] = forms.IntegerField(label=benchmark.name, min_value=0, max_value=4, required=True,
                    widget=forms.NumberInput(attrs={'type':'range', 'min': '0', 'max': '4', 'name': benchmark.name, 'class': 'form-control'}))

    def clean_deadline(self):
        deadline = self.cleaned_data['deadline']
        if datetime.date.today() >= deadline:
                raise forms.ValidationError(u'Deadline cannot be in the past: "%s"' % deadline)
        return deadline

    def process(self):
        cn = self.cleaned_data
        offer = Offer(name=cn['name'], description=cn['description'], deadline=cn['deadline'])
        offer.save()
        for benchmark in self.benchmarks:
            Rating(offer=offer, benchmark=benchmark, rating=cn['bm_%s' % benchmark.id]).save()
        return offer.id


class OfferFormView(View):
    form_class = OfferForm
    template_name = 'assessmentcenter/offer_add.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form}) 

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            offer_id = form.process()
            return HttpResponseRedirect(reverse('ac:offer_show', args=(offer_id,)))
        return render(request, self.template_name, {'form': form}) 
