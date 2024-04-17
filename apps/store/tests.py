from django.test import TestCase
from .models import Fee, Feature, Contact, Subscription
from django.urls import reverse


# Index page
class test_IndexPage(TestCase):

    # test that index page returns a 200
    def test_index_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

# Detail Page
class test_DetailPage(TestCase):

    # ran before each test.
    def setUp(self):
        highlevel = Fee.objects.create(label="high level")
        self.fee = Fee.objects.get(label='high level')

    # test that detail page returns a 200 if the item exists.
    def test_detail_page_returns_200(self):
        fee_id = self.fee.id
        response = self.client.get(reverse('store:detail', args=(fee_id,)))
        self.assertEqual(response.status_code, 200)


    # test that detail page returns a 404 if the item does not exist
    def test_detail_page_returns_404(self):

        fee_id = self.fee.id + 1
        response = self.client.get(reverse('store:detail', args=(fee_id,)))
        self.assertEqual(response.status_code, 404)

# subscription Page
class test_SubscriptionPage(TestCase):
    # ran before each test.
    def setUp(self):
        highlevel = Fee.objects.create(label="high level")
        self.fee = Fee.objects.get(label='high level')
        Contact.objects.create(lastname="Mercury",firstname="Freddie", email="fred@queen.forever",phone="451454555")
        selfdrive = Feature.objects.create(label="self driving")
        highlevel.features.add(selfdrive)
        self.contact = Contact.objects.get(firstname='Freddie')

    # test that a new subscription is made
    def test_new_subscription_is_registered(self):
        fee_id = self.fee.id
        old_subscriptions = Subscription.objects.count()
        firstname = self.contact.firstname
        lastname = self.contact.lastname
        phone = self.contact.phone
        email =  self.contact.email
        response = self.client.post(reverse('store:detail', args=(fee_id,)), {
            'firstname': firstname,
            'lastname' : lastname,
            'phone' : phone,
            'email': email
        })
        new_subscriptions = Subscription.objects.count() # count subscriptions after
        self.assertEqual(new_subscriptions, old_subscriptions + 1)

  # test that a subscription belongs to a contact
    def test_new_subscription_belongs_to_a_contact(self):
        fee_id = self.fee.id
        firstname = self.contact.firstname
        lastname = self.contact.lastname
        email =  self.contact.email
        response = self.client.post(reverse('store:detail', args=(fee_id,)), {
            'firstname': firstname,
            'lastname': lastname,
            'email': email
        })
        subscription = Subscription.objects.first()
        self.assertEqual(self.contact, subscription.contact)

    # test that a subscription belong to a fee
    def test_new_subscription_belongs_to_a_fee(self):
        fee_id = self.fee.id
        firstname = self.contact.firstname
        lastname = self.contact.lastname
        email =  self.contact.email
        response = self.client.post(reverse('store:detail', args=(fee_id,)), {
            'firstname': firstname,
            'lastname': lastname,
            'email': email
        })
        subscription = Subscription.objects.first()
        self.assertEqual(self.fee, subscription.fee)

    # test that fee counter has increased after a subscription
    def test_fee_counter_increase_if_subscribed(self):
        fee_id = self.fee.id
        old_counter= self.fee.subscripted
        firstname = self.contact.firstname
        lastname = self.contact.lastname
        email =  self.contact.email
        response = self.client.post(reverse('store:detail', args=(fee_id,)), {
            'firstname': firstname,
            'lastname': lastname,
            'email': email
        })
        # Make the query again, otherwise `available` will still be set at `True`
        self.fee.refresh_from_db()
        new_counter= self.fee.subscripted
        self.assertTrue(new_counter,old_counter+1)

    # test that fee counter has decreased after a subscription switch
    def test_fee_counter_increase_if_subscribed(self):
        #create an new fee to switch the subscription from a contact
        old_fee_id=self.fee.id
        firstname = self.contact.firstname
        lastname = self.contact.lastname
        email =  self.contact.email

        response = self.client.post(reverse('store:detail', args=(old_fee_id,)), {
            'firstname': firstname,
            'lastname': lastname,
            'email': email
        })
        old_counter= self.fee.subscripted
        
        newlevel = Fee.objects.create(label="new level")
        self.new_fee = Fee.objects.get(label='new level')
        new_fee_id = self.new_fee.id
        response = self.client.post(reverse('store:detail', args=(new_fee_id,)), {
            'firstname': firstname,
            'lastname': lastname,
            'email': email
        })
        # Make the query again, otherwise `available` will still be set at `True`
        self.fee.refresh_from_db()
        new_counter= self.fee.subscripted
        self.assertTrue(new_counter,old_counter-1)