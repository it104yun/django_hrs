from django.contrib.auth.base_user import AbstractBaseUser,BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from uuslug import slugify,uuslug
from django.utils import timezone
from django.conf import settings

from common.models import UserDefCode
from common.mixins import DictionaryMixin, AuditMixin
from common.models import GoogleLanguage

# slug-->slugify,uuslug測試--------------------------------start
class Category(DictionaryMixin, AuditMixin, models.Model):
    name = models.CharField(max_length=30, unique=True , verbose_name=_("category"))    #分類名
    title = models.CharField(max_length=30,editable=False)
    slug = models.SlugField(max_length=255,editable=False,verbose_name=_("slug"))
    slug_u1 = models.SlugField(max_length=255,editable=False,verbose_name=_("slugify(self.title)"))  # uuslug : u1-->Unicode
    slug_u2 = models.SlugField(max_length=255,editable=False,verbose_name=_("uuslug(self.title)"))   # uuslug : u2-->Unique
    slug_char = models.SlugField(max_length=255,editable=False,verbose_name=_("slug"))
    slug_char_u1 = models.SlugField(max_length=255,editable=False,verbose_name=_("char slugify(self.title)"))  # uuslug : u1-->Unicode
    slug_char_u2 = models.SlugField(max_length=255,editable=False,verbose_name=_("char uuslug(self.title)"))   # uuslug : u2-->Unique

    parent_category = models.ForeignKey('self',  blank=True, null=True,
                                        on_delete=models.CASCADE,related_name=None,
                                        verbose_name=_("parent_category"))  # 父級分類

    class Meta:
        # app_label = 'system'
        # db_table = 'Category'
        ordering = ['name']
        verbose_name = _("Category")
        verbose_name_plural = _("Categorys")
        managed = True

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title = "I love john"
        self.slug = self.title
        self.slug_u1 = slugify(self.title)
        self.slug_u2 = uuslug(self.slug_u1, instance=self, start_no=1)
        self.slug_char = self.title
        self.slug_char_u1 = slugify(self.title)
        self.slug_char_u2 = uuslug(self.slug_char_u1, instance=self, start_no=6)
        super(Category, self).save(*args, **kwargs)
        # slug-->slugify,uuslug測試--------------------------------ending


class Module(DictionaryMixin, models.Model):
    module_name = models.CharField(max_length=30, verbose_name=_("Module Name"))                        #模組名稱
    module_id = models.CharField(unique=True,max_length=30, verbose_name=_("Module Id"), null=True, blank=True)     #模組id

    class Meta:
        # app_label = 'system'
        # db_table = 'Module'
        verbose_name = _("Module")
        verbose_name_plural = _("Modules")
        managed = True

    def __str__(self):
        return self.module_name


class Program(DictionaryMixin, models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, verbose_name=_("Module"),
                               related_name='child')  # 模組
    parent = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name=_("Parent Id"),
                               blank=True, null=True, related_name='child')   # 上級
    program_id = models.CharField(primary_key=True, max_length=30,  verbose_name=_("Program ID"))        # 程式ID
    program_name = models.CharField(max_length=30, verbose_name=_("Program Name"))   # 程式名稱
    enable = models.BooleanField(verbose_name=_("Enable"), default=True)            # 啟用
    sequence = models.IntegerField(verbose_name=_("Sequence"))                      # 順序

    class Meta:
        managed = True
        # db_table = 'HrsProgram'
        verbose_name = _("Program")
        verbose_name_plural = _("Programs")
        ordering = ('module', 'sequence', 'program_id')

    def __str__(self):
        return self.program_name


    def url(self):
        return '/%s/%s' % (self.module.module_id.lower(), self.program_id)



class User(DictionaryMixin, AuditMixin, AbstractBaseUser):
    username = models.CharField(primary_key=True, max_length=8, verbose_name=_("帳號"))     #使用者帳號
    name = models.CharField(blank=True, max_length=10, verbose_name=_("姓名"))            #姓名
    last_login = models.DateTimeField(_('last_login'), default=timezone.now())
    is_admin_site = models.BooleanField(
        default=False,
        verbose_name=_('admin site urse'),
        help_text=_(
            'if can enter admin.site.urls'
        ),
    )
    is_administrator = models.BooleanField(
        default=False,
        verbose_name=_('administrator status'),
        help_text=_(
            'Designates that this user has all permissions without '
            'explicitly assigning them.'
        ),
    )

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        managed = True
        ordering = ('username',)

    def has_permission(self, program: str, factory: str) -> object or bool:
        _auth = self.auth.all()
        perm = _auth.filter(program__program__program_id=program)\
                    .filter(program__factory__id=factory)
        return perm if perm else False

    def set_unusable_password(self):
        return True

    def is_staff(self):
        return self.is_admin_site

    def is_superuser(self):
        # return True if self.username == 'MIS' else False
        # return True if self.username == 'TA190075' else False
        return self.is_administrator

    def has_module_perms(self, module):
        return True if self.username == 'TA190075' else False
        # return True if self.is_administrator == 'true' else False
        return self.is_administrator

    def has_perm(self, perm, obj=None):
        return True if self.username == 'TA190075' else False
        # return True if self.is_administrator == 'true' else False
        return self.is_administrator

    def has_perms(self, perm, obj=None):
        # return True if self.username == 'TA190075' else False
        return self.is_administrator

class UserData(DictionaryMixin, models.Model):
    user = models.OneToOneField(User, related_name="data", on_delete=models.CASCADE, verbose_name="使用者資料")
    section_manager = models.CharField(max_length=10, blank=True, null=True, verbose_name="課級主管")
    director = models.CharField(max_length=10, blank=True, null=True, verbose_name="處級主管")

    def __str__(self):
        return self.user.name

    class Meta:
        # db_table = 'UserData'
        verbose_name = 'UserData'
        verbose_name_plural = 'UserData'
        managed = True
        ordering = ('user', )



class Factory(DictionaryMixin, models.Model):
    id = models.CharField(primary_key=True, max_length=6, verbose_name=_("ID"))     #工廠ID
    name = models.CharField(max_length=50, verbose_name="公司簡稱")          #公司簡稱  2021/07/02 由60改為12
    description = models.CharField(max_length=250, verbose_name="公司全名")   #公司全名  2021/07/02 add
    nat = models.ForeignKey(UserDefCode, on_delete='CASCADE', limit_choices_to ={'topic_code':'nat_id'},
                               related_name="factory_cop_id",blank=True, null=True,verbose_name="所在地")   # 2021/07/04 add
    address = models.CharField(max_length=300, verbose_name="公司地址")    # 2021/07/04 add
    code = models.CharField(max_length=1, verbose_name="公司代碼")           #代碼

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        # db_table = 'Factory'
        verbose_name = '公司'
        verbose_name_plural = 'Factories'
        ordering = ['id']


class FactoryForegin(DictionaryMixin, models.Model):
    factory = models.ForeignKey(Factory, primary_key=True, verbose_name="公司ID", on_delete=models.CASCADE, related_name='factory_foregin')     #公司ID
    language = settings.LANGUAGES
    language_choices = language[1:len(language)]
    lang_code = models.CharField(max_length=7, choices=language_choices,verbose_name="語系")
    name = models.CharField(max_length=50, verbose_name="公司簡稱")          #公司簡稱  2021/07/02 由60改為12
    description = models.CharField(max_length=200, verbose_name="公司全名")   #公司全名  2021/07/02 add
    address = models.CharField(max_length=300, verbose_name="公司地址")    # 2021/07/04 add

    def __str__(self):
        return self.name

    class Meta:
        managed = True


class FactoryProgram(DictionaryMixin, models.Model):
    factory = models.ForeignKey(Factory, verbose_name="公司ID", on_delete=models.CASCADE, related_name='program')     #公司ID
    program = models.ForeignKey(Program, verbose_name="程式ID", on_delete=models.CASCADE, related_name='factory')     #程式ID

    class Meta:
        # db_table = 'FactoryProgram'
        verbose_name = 'FactoryProgram'
        verbose_name_plural = 'FactoryPrograms'
        managed = True
        ordering = ('factory', 'program')

    def __str__(self):
        return self.program.program_name


class FactoryAuth(DictionaryMixin, AuditMixin, models.Model):
    user = models.ForeignKey(User, verbose_name=_("User ID"), on_delete=models.CASCADE, related_name="factory")     #使用者ID
    factory = models.ForeignKey(Factory, verbose_name="公司ID", on_delete=models.CASCADE, related_name="user")        #公司ID

    class Meta:
        # db_table = 'FactoryAuth'
        verbose_name = 'FactoryAuth'
        verbose_name_plural = 'FactoryAuth'
        managed = True


class ProgramAuth(DictionaryMixin, AuditMixin, models.Model):
    program = models.ForeignKey(FactoryProgram, on_delete=models.CASCADE,
        verbose_name=_("Program ID"), related_name="auth")               #程式ID
    user = models.ForeignKey(User, on_delete=models.CASCADE,
        verbose_name=_("User ID"), related_name="auth")                  #使用者ID
    create = models.BooleanField(verbose_name=_("Add"))                  #新增
    delete = models.BooleanField(verbose_name=_("Delete"))               #刪除
    update = models.BooleanField(verbose_name=_("Edit"))                 #修改
    read = models.BooleanField(verbose_name=_("Read"))                   #讀取
    self_data = models.BooleanField(verbose_name=_("Self Data"))         #自己的資料
    all_data = models.BooleanField(verbose_name=_("All Data"))           #所有的資料

    class Meta:
        # db_table = 'ProgramAuth'
        verbose_name = 'ProgramAuth'
        verbose_name_plural = 'ProgramAuths'
        unique_together = ('program', 'user')
        managed = True
        ordering = ('program', 'user')


