from PIL import Image
from django import forms
from filer.models import File,Folder
from core.custom_forms_fields import DataFileField,PhotoFileField
from django.utils.translation import ugettext_lazy as _
from core.utils import is_image, is_data
from django.core.files.storage import default_storage
from tagulous.forms import TagField
from tagulous.models import TagOptions
from tag.models import TagSubject



class CropForm(forms.ModelForm):
    """
    Crop a photo when input
    """
    #https://simpleisbetterthancomplex.com/tutorial/2017/03/02/how-to-crop-images-in-a-django-application.html
    class Meta:
        model = File
        fields = ('file', 'x', 'y', 'width', 'height')

    x = forms.FloatField(required=False,widget=forms.HiddenInput(attrs={'id':'id_x','name':'x'}))
    y = forms.FloatField(required=False,widget=forms.HiddenInput(attrs={'id':'id_y','name':'y'}))
    width = forms.FloatField(required=False,widget=forms.HiddenInput(attrs={'id':'id_width','name':'width'}))
    height = forms.FloatField(required=False,widget=forms.HiddenInput(attrs={'id':'id_height','name':'height'}))
    file = PhotoFileField(required=False,widget=forms.FileInput(attrs={'id':'id_file','name':'file'}))

    def save(self,commit=True):
        #import ipdb; ipdb.set_trace()
        files=self.files.getlist('file')
        croplist=[]
        for file in files:
            crop = File(file=file, name=file.name)
            image = Image.open(file)
            if len(files)>1:
                w=image.width
                h=image.height
                s=min(w,h)
                x,y=int((w-s)/2),int((h-s)/2)
                w,h=s,s
            else:
                x = self.cleaned_data.get('x')
                y = self.cleaned_data.get('y')
                w = self.cleaned_data.get('width')
                h = self.cleaned_data.get('height')

            cropped_image = image.crop((x, y, w+x, h+y))
            resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
            from django.core.files.base import ContentFile
            from io import BytesIO
            image_io = BytesIO()
            resized_image.save(image_io, format=image.format)
            name = crop.file.name
            crop.file.save(name,content=ContentFile(image_io.getvalue()),save=False)
            crop.save()
            #dest=default_storage.open(name=crop.file.name,mode="wb")
            #resized_image.save(dest)
            #dest.close()
            croplist.append(crop)
        return croplist

    def clean_file(self):
        files = self.files.getlist('file')
        errors=[]
        for file in files:
            if file:
                if not is_image(file):
                    errors.append("'{}' {}".format(file.name,_("is not a valid image")))
            else:
                errors.append(_("Could not read the uploaded file."))
        if errors:
            raise forms.ValidationError(errors)
        return

class DataFileForm(forms.ModelForm):
    file = DataFileField(widget=forms.FileInput(attrs={'id':'id_file','name':'file'}))
    class Meta:
        model = File
        fields = ('file',)

    def save(self,commit=True):
        files=self.files.getlist('file')
        filelist = [File.objects.create(file=file, name=file.name) for file in files]
        return filelist

    def clean_file(self):
        #import ipdb; ipdb.set_trace()
        files = self.files.getlist('file')
        errors=[]
        for file in files:
            if file:
                if not is_data(file):
                    errors.append("'{}' {}".format(file.name,_("is not a valid data file")))
            else:
                errors.append(_("Could not read the uploaded file."))
        if errors:
            raise forms.ValidationError(errors)
        return


class FolderForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(FolderForm,self).__init__(*args,**kwargs)
        self.fields['description'].strip=False

    class Meta:
        model = Folder
        fields=('name','description')

class FileForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(FileForm,self).__init__(*args,**kwargs)
        self.fields['description'].strip=False

    class Meta:
        model = File
        fields = '__all__'


class FileShortForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('name','is_favorite','description')

    name = forms.CharField(
        label='title',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': _('title of the file'), 'id':'id_file_name'}),
        required=True
        )

    is_favorite=forms.BooleanField(
        #label = _('tag as favorite'),
        required=False,
        label_suffix='',
        widget=forms.CheckboxInput(attrs={'id':'id_file_favorite','class':'fl-crown' }))

    description = forms.CharField(
        #label='description',
        max_length=1000,
        widget=forms.Textarea(attrs={'placeholder': _('type a description'), 'id':'id_file_description','onkeyup':"textCount(this);",'resize':'none', 'class':'w-100'}),
        required=False
        )



class FileSubjectsForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('subjects',)

    subjects=TagField(
        required=False,
        tag_options=TagOptions(
        force_lowercase=True,
        ),
        autocomplete_tags=TagSubject.objects.autocomplete_most_frequent()
    )
