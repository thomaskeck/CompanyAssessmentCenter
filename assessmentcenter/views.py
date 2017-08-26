import datetime

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic, View
from django.db.models import Count, Avg, F, FloatField, Sum

from django.utils.dateparse import parse_datetime
from django import forms

from .models import Benchmark, Offer, Rating


class OfferListView(generic.ListView):
    def get_queryset(self):
        weighted_avg = (Sum(F('rating__rating')*F('rating__benchmark__weight'), output_field=FloatField()) 
                       / Sum(F('rating__benchmark__weight'), output_field=FloatField()))
        return Offer.objects.order_by('deadline').annotate(weighted_avg=weighted_avg)


class OfferDetailView(generic.DetailView):
    model = Offer
    

class OfferForm(forms.Form):
    name = forms.CharField(label='Offer Name', min_length=1, max_length=100, strip=True, required=True)
    description = forms.CharField(label='Offer Description', max_length=10000, widget=forms.Textarea)
    deadline = forms.DateField(label='Deadline', required=True,
                               widget=forms.DateInput(attrs={'type':'date'}))

    def __init__(self, *args, **kwargs):
        super(OfferForm, self).__init__(*args, **kwargs)
        self.benchmarks = Benchmark.objects.order_by('weight')
        for benchmark in self.benchmarks:
            self.fields['bm_%s' % benchmark.id] = forms.IntegerField(label=benchmark.name, min_value=0, max_value=4, required=True,
                    widget=forms.NumberInput(attrs={'type':'range', 'min': '0', 'max': '4', 'name': benchmark.name, 'class': 'form-control'}))
        self.fields['offer_id'] = forms.IntegerField(label="", widget=forms.HiddenInput())
        self.fields['offer_id'].initial = 0

    def init_fields(self, pk):
        offer = Offer.objects.get(pk=pk)
        self.fields['name'].initial = offer.name
        self.fields['description'].initial = offer.description
        self.fields['deadline'].initial = str(offer.deadline.date() + datetime.timedelta(days=1))
        self.fields['offer_id'].initial = pk
        for rating in offer.rating_set.all():
            self.fields['bm_%s' % rating.benchmark.id].initial = rating.rating

    def clean_deadline(self):
        deadline = self.cleaned_data['deadline']
        if datetime.date.today() >= deadline:
                raise forms.ValidationError(u'Deadline cannot be in the past: "%s"' % deadline)
        return deadline

    def create_offer(self):
        cn = self.cleaned_data
        offer = Offer(name=cn['name'], description=cn['description'], deadline=cn['deadline'])
        offer.save()
        for benchmark in self.benchmarks:
            Rating(offer=offer, benchmark=benchmark, rating=cn['bm_%s' % benchmark.id]).save()
        return offer.id

    def update_offer(self):
        cn = self.cleaned_data
        offer = Offer.objects.get(pk=cn['offer_id'])
        offer.name = cn['name']
        offer.description = cn['description']
        offer.deadline = cn['deadline']
        offer.save()

        ratings = offer.rating_set.all()
        for benchmark in self.benchmarks:
            for rating in ratings:
                if rating.benchmark == benchmark:
                    break
            else:
                rating = Rating(offer=offer, benchmark=benchmark, rating=0)
            rating.rating = cn['bm_%s' % benchmark.id]
            rating.save()
        return offer.id


class OfferCreateView(View):
    form_class = OfferForm
    template_name = 'assessmentcenter/offer_form.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form}) 

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            offer_id = form.create_offer()
            return HttpResponseRedirect(reverse_lazy('ac:offer_detail', args=(offer_id,)))
        return render(request, self.template_name, {'form': form})


class OfferUpdateView(View):
    form_class = OfferForm
    template_name = 'assessmentcenter/offer_form.html'

    def get(self, request, pk, *args, **kwargs):
        form = self.form_class()
        form.init_fields(pk)
        return render(request, self.template_name, {'form': form}) 

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            offer_id = form.update_offer()
            return HttpResponseRedirect(reverse_lazy('ac:offer_detail', args=(offer_id,)))
        return render(request, self.template_name, {'form': form})


class OfferDeleteView(generic.edit.DeleteView):
    model = Offer
    success_url = reverse_lazy('ac:offer_list')


class BenchmarkListView(generic.ListView):
    def get_queryset(self):
        return Benchmark.objects.order_by('weight')


class BenchmarkDetailView(generic.DetailView):
    model = Benchmark


class BenchmarkCreateView(generic.edit.CreateView):
    model = Benchmark
    fields = ['name', 'weight']
    success_url = reverse_lazy('ac:benchmark_list')


class BenchmarkUpdateView(generic.edit.UpdateView):
    model = Benchmark
    fields = ['name', 'weight']
    success_url = reverse_lazy('ac:benchmark_list')


class BenchmarkDeleteView(generic.edit.DeleteView):
    model = Benchmark
    success_url = reverse_lazy('ac:benchmark_list')
