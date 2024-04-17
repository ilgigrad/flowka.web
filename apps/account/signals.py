from account.models import User,Team,UserProfile,TeamProfile
from account.perms import Perm,Holder
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from core.utils import Const
from filer.models import Folder,File


def create_user(sender, instance, created, **kwargs):
    if created:
        #create an instance of userprofile
        UserProfile.objects.create(user=instance)
        #create Holder
        holder=Holder.objects.create(is_user=True)
        instance.holder=holder
        instance.save()
        #create a void team associated to the new user
        connectTeam=Team.objects.create(
            name=Team.TEAM_NAMES.get_value('connected'),
            access='personal'
            )
        suggestTeam=Team.objects.create(
            name=Team.TEAM_NAMES.get_value('suggested'),
            access='personal'
            )
        blockTeam=Team.objects.create(
            name=Team.TEAM_NAMES.get_value('blocked'),
            access='personal'
            )
        #affect user and perm to that new team
        connectTeam.user.add(instance)
        suggestTeam.user.add(instance)
        blockTeam.user.add(instance)
        #create a new permission for that holder
        connectTeam.access_perms(instance.holder)
        suggestTeam.access_perms(instance.holder)
        blockTeam.access_perms(instance.holder)
        #create folders
        myFiles=Folder.objects.create(
            name="all my files",
            is_root=True,
            parent=None,
            icon=Const.ICON['folders'],
            color=Const.COLOR['white'],
            is_public=False,
            description='all files of ' + instance.email,
            owner=instance
        )
        myFiles.access_perms([instance.holder])
        myFiles.remove_perms([instance.holder],['can_remove'])
        favorites=Folder.objects.create(
            name="favorites",
            is_root=True,
            parent=None,
            icon=Const.ICON['crown'],
            color=Const.COLOR['anis'],
            is_public=False,
            description='favorites files of ' + instance.email,
            owner=instance
        )
        favorites.access_perms([instance.holder])
        favorites.remove_perms([instance.holder],['can_add'])
        shared=Folder.objects.create(
            name="shared",
            is_root=True,
            parent=None,
            icon=Const.ICON['share-alt'],
            color=Const.COLOR['rose'],
            is_public=False,
            description='files shared with ' + instance.email,
            owner=instance
        )
        shared.access_perms([instance.holder])
        shared.remove_perms([instance.holder],['can_add'])

def delete_user(sender, instance, **kwargs):
    #suppress teams where the user was the unique user
    holder=instance.holder
    if holder is not None:
        instance.holder=None
        Team.objects.filter(perms__holder=holder).prefetch_related('perms').delete() #delete perms on Team associated with the user
        Folder.objects.filter(perms__holder=holder).prefetch_related('perms').delete() #delete perms on File associated with the user
        File.objects.filter(perms__holder=holder).prefetch_related('perms').delete() #delete perms on Folder associated with the user
        holder.delete()
    Team.objects.personal_team(instance).delete()#suppress teams with 'personal' status  for the user

def create_team(sender, instance, created, **kwargs):
    # #create basic permissions for the user who creates the team
    if created:
        TeamProfile.objects.create(team=instance)
        holder=Holder.objects.create(is_user=False)
        instance.holder=holder
        instance.save()

def delete_team(sender, instance, **kwargs):
    instance.user.clear()
    instance.perms.clear()
    holder=instance.holder
    if holder is not None:
        instance.holder=None
        holder.delete()
    #     user.clean_perms(instance)
    # Perm.objects.del_perms(instance)

post_save.connect(create_user,sender=User )
post_save.connect(create_team, sender=Team)
pre_delete.connect(delete_user, sender=User)
pre_delete.connect(delete_team, sender=Team)
