from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
import urllib.request
import json
from .models import Thing, Person


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'person_list'

    def get_queryset(self):
        """
        Return the last five published questions 
        (not including those set to be
        published in the future).
        """
        return Person.objects.all()


class ThingsListView(generic.ListView):
    template_name = 'polls/thingslist.html'
    context_object_name = 'latest_things_list'

    def get_queryset(self):
        """
        Return the last five published questions 
        (not including those set to be
        published in the future).
        """
        return Thing.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')

def detail(request, thing_id):
    thing = get_object_or_404(Thing, pk=thing_id)
    return render(request, 'polls/detail.html', {'thing': thing, 'person_list': Person.objects.all()})


def person_detail(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    spendings = 0
    for thing in person.thing_set.all():
        spendings += thing.price
    person.spendings = spendings
    

    overall_spendings = 0
    for pers_spendings in Person.objects.all():
        overall_spendings += pers_spendings.spendings
    person.net_spendings = spendings - (overall_spendings / Person.objects.count())

    person.save()
    return render(request,
                  'polls/person_detail.html',
                  {'person': person,
                   "thing_set": person.thing_set.all(),
                   'person_list': Person.objects.all()})

    


def new(request):
    return render(
                request,
                'polls/new.html',
                {'thing': Thing, 'person_list': Person.objects.all()}
                ) 


CZK_to_EUR = 25.5
def vote(request):
    good = request.POST['thing_name']
    zboziURL = "https://www.zbozi.cz/api/v1/search?categoryLoadOffers=1&forceListProductsAndOffers=0&groupByCategory=0&groupByCategoryProductCount=4&loadTopProducts=false&page=1&query="
    with urllib.request.urlopen((zboziURL + good.replace(' ', '-'))) as url:
        data = json.loads(url.read().decode())
        meanPrice = 0
    try:
        for i in range(1, len(data['products']) + 1):
            meanPrice = meanPrice + data['products'][i - 1]['minPrice']
        meanPrice = meanPrice / (len(data['products']) + 1) / 100
        found_price = round(meanPrice, 2)
        flag = 1
    except:
        try:
            results = 0
            meanAppPrice = 0
            for i in range(1, len(data['priceRanges'])):
                results = results + data['priceRanges'][i - 1]['results']
                meanAppPrice = meanAppPrice + \
                    ((data['priceRanges'][i - 1]['minPrice'] + data['priceRanges']
                      [i - 1]['maxPrice']) / 2) * (data['priceRanges'][i - 1]['results'])
            meanAppPrice = meanAppPrice / results
            found_price = round(meanAppPrice, 2)
            flag = 2
        except:
            found_price = 0
            flag = 3
    p = Person.objects.get(pk=request.POST['buyer'])
    price = request.POST['thing_price']
    t = Thing(
        thing_description=good,
        pub_date=timezone.now(),
        price=price,
        found_price=(found_price / CZK_to_EUR),
        buyer=p,
        flag=flag
        )
    t.save()
    p.spendings += float(price)
    p.save()
    return HttpResponseRedirect(reverse('polls:index'))
