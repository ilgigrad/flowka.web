from filer.models import File,Folder
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete

def create_file(sender, instance, created, **kwargs):
    if created:
        pass

def create_folder(sender, instance, created, **kwargs):
    if created:
        pass

def delete_file_or_folder(sender, instance, **kwargs):
        owner=instance.owner
        instance.perms.clear()

post_save.connect(create_folder,sender=Folder )
post_save.connect(create_file, sender=File)
pre_delete.connect(delete_file_or_folder, sender=File)
pre_delete.connect(delete_file_or_folder, sender=Folder)
