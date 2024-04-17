from django.conf.urls import url
from django.urls import reverse_lazy
from . import views as account_views
from django.contrib.auth import views as auth_views # import views so we can use them in urls.

app_name = 'account'


urlpatterns = [

    url(r'^login/$',
        account_views.LoginView.as_view(),
    name='login'),

    url(r'^logout/$',
        account_views.logout,
    name='logout'),

    url(r'^password_change/$',
        auth_views.PasswordChangeView.as_view(
        template_name='account/password_change.html',
        success_url=reverse_lazy('account:password_change_done'),
        extra_context={'homebg':True}),
    name='password_change'),

    url(r'^password_change_done/$',
        account_views.password_change_done,
    name='password_change_done'),

    url(r'^password_reset/$',
        auth_views.PasswordResetView.as_view(
        template_name='account/password_reset.html',
        email_template_name='account/password_reset_email.html',
        subject_template_name='account/password_reset_subject.txt',
        success_url=reverse_lazy('account:password_reset_done'),
        from_email='noreply@ilgigrad.net',
        extra_context={'homebg':True}),
    name='password_reset'),

    url(r'^password_reset_done/$',
        account_views.password_reset_done,
    name='password_reset_done'),

    url(r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.PasswordResetConfirmView.as_view(
        template_name='account/password_reset_confirm.html',
        success_url=reverse_lazy('account:password_change_done'),
        extra_context={'homebg':True}),
    name='password_reset_confirm'),


    url(r'^signup/$',
        account_views.signup,
    name='signup'),

    url(r'^signup/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        account_views.activate,
    name='activate'),

    url(r'^profile/$',
        account_views.ProfileView.as_view(),
    name='profile'),
]
