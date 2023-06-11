from django.shortcuts import render
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect, HttpResponse
from .models import Month, Sort, Faq, Article, Agreement, Region, Amount
from .forms import ContactForm, PhotographersForm, TreeAdoptionForm, OrderForm

# Create your views here.

def index(request):
    page_title = 'Бахчисарайский персик | Главная'
    ctx = {'page_title': page_title}
    return render (request, 'base/index.html', ctx)

def about(request):
    page_title = 'Бахчисарайский персик | О нас'
    ctx = {'page_title': page_title}
    return render (request, 'base/about.html', ctx)

def sorts(request):
    page_title = 'Бахчисарайский персик | Сорта'
    months = Month.objects.all()

    cat = request.GET.get('cat')
    if cat == None:
        sorts = Sort.objects.all()
    else:
        sorts = Sort.objects.filter(cat__title=cat)   


    ctx = {'page_title': page_title, 'months': months, 'sorts': sorts, 'cat': cat}
    return render(request, 'base/sorts.html', ctx)


def grow(request):
    page_title = 'Как мы выращиваем | Бахчисарайский персик'
    articles = Article.objects.all()[1:2]

    ctx = {'page_title': page_title, 'articles': articles}
    return render(request, 'base/growing.html', ctx)

def facts(request):
    page_title = 'Бахчисарайский персик | F.A.Q'
    facts = Faq.objects.all()
    articles = Article.objects.all()[:1]

    ctx = {'page_title': page_title, 'facts': facts, 'articles': articles}
    return render(request, 'base/faq.html', ctx)

def pickup(request):
    page_title = 'Бахчисарайский персик | Самовывоз'        
    ctx = {'page_title': page_title}
    return render(request, 'base/pickup.html', ctx)

def delivery(request):
    page_title = 'Бахчисарайский персик | Доставка'
    regions = Region.objects.all()

    # обработка формы заказа

    submitted=False
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            order_name = cd['name']
            order_email = cd['email']
            order_phone = cd['phone']
            order_region = cd['region']
            order_address = cd['address']
            order_amount = cd['amount']
            order_is_combined = cd['is_combined']
        
            html = render_to_string('base/mails/orderform.html', 
                                {
                                    'name': order_name,
                                    'email': order_email,
                                    'phone': order_phone,
                                    'region': order_region,
                                    'address': order_address,
                                    'amount': order_amount,
                                    'is_combined' : order_is_combined,
                                    }
                                )
            order = EmailMessage('Новый заказ', body=html,
                                to=[
                                    'minich.songwriter@yandex.ru',
                                    '79787308387@ya.ru'
                                    ])
            order.content_subtype='html'
            order.send()

            return HttpResponseRedirect('?submitted=True')
    else:
        form = OrderForm()
        if 'submitted' in request.GET:
            submitted=True
        
    ctx = {'page_title': page_title, 'regions': regions, 
           'form': form, 'submitted': submitted}
    return render(request, 'base/delivery.html', ctx)


def load_amount(request):
    region_id = request.GET.get('region')
    amounts = Amount.objects.filter(region_id=region_id)
    ctx = {'amounts': amounts}
    return render (request, 'base/partials/load_amount.html', ctx)

def collection(request):
    page_title = 'Бахчисарайский персик | Самосбор'

    ctx = {'page_title': page_title}
    return render(request, 'base/self-collection.html', ctx)
    
def adoption(request):
    page_title = 'Бахчисарайский персик | Усынови персик'

    #sending form
    submitted = False

    if request.method == 'POST':
        form = TreeAdoptionForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            mess_team_name = cd['team_name']
            mess_team_leader = cd['team_leader']
            mess_email = cd['email']
            mess_phone = cd['phone']
            mess_team_mates_count = cd['team_mates_count']
            mess_sort_choose = cd['sorts']
            mess_trees_count = cd['trees_count']
            
        html = render_to_string('base/mails/adoptionform.html',
                                {
                                    'team_name': mess_team_name,
                                    'team_leader': mess_team_leader,
                                    'email': mess_email,
                                    'phone': mess_phone,
                                    'team_mates_count': mess_team_mates_count,
                                    'sorts': mess_sort_choose,
                                    'trees_count': mess_trees_count,
                                })
        mess = EmailMessage('Заявка на усыновление персика', body=html, 
                            to=[
                                'minich.songwriter@yandex.ru', 
                                '79787308387@ya.ru',
                                ])
        mess.content_subtype = 'html'
        mess.send()

        return HttpResponseRedirect('?submitted=True')
    else:
        form = TreeAdoptionForm()
        if 'submitted' in request.GET:
            submitted = True

    ctx = {'page_title': page_title, 'form': form, 'submitted': submitted}
    return render(request, 'base/peach-adoption.html', ctx)

def photographers(request):
    page_title = 'Бахчисарайский персик | Фотографам'
    points = Agreement.objects.all()
    
    # sending form
    submitted = False 
    if request.method == 'POST':
        form = PhotographersForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            mess_name = cd['name']
            mess_surname = cd['surname']
            mess_email = cd['email']
            mess_phone = cd['phone']
            mess_date = cd['date']
            mess_time = cd['time']
            mess_participants = cd['participants']
            mess_duration = cd['duration']

        html = render_to_string('base/mails/photoform.html',
                                {
                                    'name': mess_name,
                                    'surname': mess_surname,
                                    'email': mess_email,
                                    'phone': mess_phone,
                                    'date': mess_date,
                                    'time': mess_time,
                                    'participants': mess_participants,
                                    'duration': mess_duration,
                                })
        mess = EmailMessage('Заявка на фотосъёмку', body=html, 
                            to=['minich.songwriter@yandex.ru', '79787308387@ya.ru'])
        mess.content_subtype = 'html'
        mess.send()

        return HttpResponseRedirect('?submitted=True')
    else:
        form = PhotographersForm()
        if 'submitted' in request.GET:
            submitted=True

    ctx = {'page_title': page_title, 'points': points, 'form': form, 'submitted': submitted}
    return render(request, 'base/photographers.html', ctx)

def contacts(request):
    page_title = 'Бахчисарайский персик | Контакты'

    # sending form
    submitted = False 
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            mess_subject = cd['subject']
            mess_name = cd['name']
            mess_email = cd['email']
            mess_phone = cd['phone']
            mess_message = cd['message']

        html = render_to_string('base/mails/contactform.html', \
                                {
                                    'subject': mess_subject,
                                    'name': mess_name,
                                    'email': mess_email,
                                    'phone': mess_phone,
                                    'message': mess_message,
                                })
        mess = EmailMessage(mess_subject, body=html, 
                            to=['minich.songwriter@yandex.ru', '79787308387@ya.ru'])
        mess.content_subtype = 'html'
        mess.send()

        return HttpResponseRedirect('?submitted=True')
    else:
        form = ContactForm()
        if 'submitted' in request.GET:
            submitted=True
    
    ctx = {'page_title': page_title, 'form': form, 'submitted': submitted}
    return render (request, 'base/contacts.html', ctx)