from django import forms

class EnumMixin(object):

  @classmethod
  def get_value(cls,member):
      try:
          return cls[member].value[0]
      except:
        return None


class NextFormMixin(forms.Form):
    """
    add a 'next' hidden input field into forms in order to manage redirect to previous page
    """
    next = forms.CharField(max_length=100, widget=forms.HiddenInput())
    def __init__(self, *args, **kwargs):
        #import ipdb; ipdb.set_trace()
        next = kwargs.pop('next',None)
        super(NextFormMixin,self).__init__(*args,**kwargs)
        try:
            self.fields['next'].initial = next
        except:
            pass
