def group_required(*group_names):
   """Requires user membership in at least one of the groups passed in."""

   def in_groups(u):
       if u.is_authenticated():
           if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
               return True
       return False
   return user_passes_test(in_groups)


from django.http import HttpResponseForbidden


logger = logging.getLogger(__name__)


def user_can_write_a_review(func):
   """View decorator that checks a user is allowed to write a review, in negative case the decorator return Forbidden"""

   @functools.wraps(func)
   def wrapper(request, *args, **kwargs):
       if request.user.is_authenticated() and request.user.points < 10:
           logger.warning(
            'The {} user has tried to write a review, but does not have enough points to do so'.format( request.user.pk))
           return HttpResponseForbidden()

       return func(request, *args, **kwargs)

   return wrapper
