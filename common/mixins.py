from django.db import models
from django.db.models.fields import DateTimeField, CharField, BooleanField
from django.utils.translation import gettext_lazy as _

from django.db.models.fields.related import (
    ForeignKey,
    ManyToManyField,
    OneToOneField,
)
from django.utils import timezone
to_tz = timezone.get_default_timezone()


class DictionaryMixin:
    """Provide to_dict function to wrap model datas into a dictionary."""

    def to_dict(self, related=True):
        """
        Includes both field values and related pk if related is True.
        Otherwise it will only include field value.
        """
        data = dict()
        opt = self._meta.concrete_fields
        for field in opt:
            q = getattr(self, field.name)
            if isinstance(field, DateTimeField):
                parse_time = q.astimezone(to_tz).strftime("%Y-%m-%d %H:%M")\
                    if q else ''
                data[field.name] = parse_time
            elif (isinstance(field, ForeignKey) or
                  isinstance(field, ManyToManyField) or
                  isinstance(field, OneToOneField)):
                if related and q:
                    data[field.name] = q.__str__()
                    data['%s_id' % field.name] = q.pk
                else:
                    data[field.name] = q.__str__()
            elif isinstance(field, CharField) and field.choices:
                ch = field.choices
                try:
                    display = [c[1] for c in ch if c[0] == q][0]
                except IndexError as e:
                    display = ''

                if related:
                    data[field.name] = display
                    data['%s_id' % field.name] = q
                else:
                    data[field.name] = display
            elif isinstance(field, BooleanField):
                data[field.name] = str(q).capitalize()
            else:
                data[field.name] = q

        return data


class AuditMixin(models.Model):
    # URRF = models.CharField(default='',max_length=15, blank=True, null=True, verbose_name="User Reserved Reference")
    # URRF1 = models.CharField(default='',max_length=30, blank=True, null=True, verbose_name="User Reserved Reference1")
    # URRF2 = models.CharField(max_length=30, blank=True, null=True, verbose_name="User Reserved Reference2")
    creator = models.CharField(max_length=10,auto_created=True,editable=False,verbose_name=_("Creator"))    #第一次建立時, 才始用default
    create_time = models.DateTimeField(db_index=True,auto_now_add=True,editable=False,verbose_name=_("Create Time"))
    changer = models.CharField(max_length=10,auto_created=True,editable=False,verbose_name=_("Changer"))    #到時候, 若修改更改此欄位
    change_time = models.DateTimeField(auto_now_add=True,editable=False,verbose_name=_("Change Time"))
    '''
        URCD1 = models.CharField(max_length=2, blank=True, null=True, verbose_name="User Defined Codes1")
        URCD2 = models.CharField(max_length=4, blank=True, null=True, verbose_name="User Defined Codes2")
        URDT1 = models.DateTimeField(blank=True, null=True, verbose_name="User Defined DateTime1")
        URDT2 = models.DateTimeField(blank=True, null=True, verbose_name="User Defined DateTime1")
        URAB1 = models.IntegerField(blank=True, null=True,verbose_name="User Reserved Number1")
        URAB2 = models.IntegerField(blank=True, null=True, verbose_name="User Reserved Number1")
        URAT1 = models.DecimalField(max_length=11, max_digits=8, decimal_places=2, blank=True, null=True, verbose_name="User Reserved Amount1")   # 11.2 小數點佔一位
        URAT2 = models.DecimalField(max_length=17, max_digits=12, decimal_places=4, blank=True, null=True, verbose_name="User Reserved Amount2")  # 17.4 小數點佔一位

        name_host = models.CharField(max_length=20,verbose_name="Host name",default='GM6020')
        name_app = models.CharField(max_length=20,verbose_name="App name")
        name_view = models.CharField(max_length=20,verbose_name="View name")
    '''


    class Meta:
        abstract = True

