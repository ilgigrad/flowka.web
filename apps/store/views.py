from django.shortcuts import  get_object_or_404
#from django.http import HttpResponse
from django.template import loader
from django.template.response import TemplateResponse
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from .forms import ContactForm, SubscriptForm
from .models import Fee, Feature, Contact, Subscription
from django.db import transaction, IntegrityError
from django.utils.translation import ugettext as _
from django.core.mail import EmailMessage




def pricing(request):
    fees=Fee.objects.filter(available=True).order_by('price')[:12]
    context = {'fees' : fees}
    return TemplateResponse(request,'store/pricelist.html', context)


def detail(request, fee_id):
    #fee = Fee.objects.get(pk=fee_id)
    #features = " ".join([feature.label for feature in fee.features.all()])
    #message = "Fee {}. contains features : {}".format(fee.label, features)
    #return HttpResponse(message)
    fee=get_object_or_404(Fee,pk=fee_id)
    context = {'fee' : fee}

    #test if form as been post
    if request.method == 'POST':
        form = SubscriptForm(request.POST)
        #form has no error
        if form.is_valid():
            email     = form.cleaned_data['email']
            lastname  = form.cleaned_data['lastname']
            firstname = form.cleaned_data['firstname']
            phone     = form.cleaned_data['phone']
            # search if the contact already exists
            try:
                with transaction.atomic():
                    contact = Contact.objects.filter(email=email)
                    if not contact.exists():
                        # If a contact is not registered, create a new one.
                        contact = Contact.objects.create(
                            email      = None if email is None else email.lower(),
                            firstname  = None if firstname is None else firstname.lower(),
                            lastname   = None if lastname is None else lastname.lower(),
                            phone      = None if phone is None else phone.lower()
                        )
                    #if contact exists verify if there is a previous subscription
                    else:
                        contact=contact.first()
                        oldsubscription = Subscription.objects.filter(contact=contact)
                        #if previous subscription (subscrapt the fee counter and delete the old subscription)
                        if oldsubscription.exists():
                            oldsubscription=oldsubscription.first()
                            # oldfee=oldsubscription.fee
                            # oldfee.subscripted-=1
                            # oldfee.save()
                            oldsubscription.delete()
                            context['update']=True
                    # then create a new subscitption for the contact
                    subscription = Subscription.objects.create(
                        contact=contact,
                        fee=fee
                    )
                    #update the fee subscription counter
                    # if fee.subscripted is None:
                    #     fee.subscripted=1
                    # else:
                    #     fee.subscripted+=1
                    # fee.save()
                    context ['contact']=contact
                    return TemplateResponse(request,'store/thanksbuying.html', context)
            except IntegrityError:
                form.errors['internal'] = _("an internal error has raised. Please try again.")
            # Form data doesn't match the expected format.
            # Add errors to the template.
    #was not a form post answer/ the page is caled for the first time
    else:
        form = SubscriptForm()
    context ['form']= form
    context['errors'] = form.errors.items()
    return TemplateResponse(request,'store/detail.html', context)

def search(request):
    query = request.GET.get('query')
    if not query:
        fees=Fee.objects.all()
    else:
        fees = Fee.objects.filter(label__icontains=query)

        if not fees.exists(): #if not in album label... search on features label
            fees=Fee.objects.filter(features__label__icontains=query)
    context = {'fees' : fees}
    return TemplateResponse(request,'store/search.html', context)

def index(request):
    return TemplateResponse(request,'store/index.html')

#def index(request):
#     fees=Fee.objects.filter(available=True).order_by('price')[:12]
#     formated_fees=["<li>{}</li>".format(fee.label) for fee in fees]
#     message="hello"
#     return HttpResponse(message)

def listing(request):
    features_list = Feature.objects.all()
    paginator = Paginator(features_list, 5)
    page = request.GET.get('page')
    try:
        features = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        features = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        features = paginator.page(paginator.num_pages)
    context = {
        'features': features,
        'paginate': True
    }
    return TemplateResponse(request,'store/listing.html', context)


def contact(request):

    #test if form as been post
    context={}
    context['homebg']=True
    if request.method == 'POST':
        form = ContactForm(request.POST)
        #form has no error
        if form.is_valid():
            email     = form.cleaned_data['email']
            subject  = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            try:
                email_to_send = EmailMessage(
                    subject,
                    message,
                    email,
                    ['contact@flowka.com',email],
                    [],
                    reply_to=[email],
                    )
                email_to_send.send()
                context['title']='Contact'
                info={'title':'Contact!','desc':_('Your message has been saved<br> You will receive a copy of it at {} '.format(email))}
                context['info']=info
                return TemplateResponse(request,'info.html', context)
            except IntegrityError:
                form.errors['internal'] = _("an internal error has raised. Please try again.")
        else:
            context['errors'] = form.errors.items()
    form = ContactForm()
    context ['form']= form
    return TemplateResponse(request,'store/contact.html', context)
