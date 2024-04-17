from django.db import models


class ColumnManager (models.Manager):

    def onetarget(self,instance):
        #import ipdb; ipdb.set_trace()
        if instance.target:
            instance.drop_column=False
            targets=self.filter(dataset=instance.dataset,target=True).exclude(id=instance.id)
            for target in targets:
                target.target=False
                target.save()
        return instance.target
