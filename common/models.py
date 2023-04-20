from django.utils.translation import gettext_lazy as _

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.db.models import F, Q
from .mixins import DictionaryMixin, AuditMixin
from django.core.validators import MaxValueValidator, MinValueValidator
import googletrans
from django.utils import timezone
from django.conf import settings

current_tz = timezone.get_current_timezone()
now = timezone.now().astimezone(current_tz).strftime('%Y-%m-%d')

choice_language = settings.LANGUAGES

#使用者自定義碼的主題-IT使用
class TopicOfUdc(DictionaryMixin, AuditMixin, models.Model):
    topic_code = models.CharField(primary_key=True,max_length=30,verbose_name=_('Topic Code'))  # 應為存在的欄名(model field_name)
                                                                                               # 設計form時, 可設計只能挑field_name
                                                                                               # 日後若技術成熟時,開一個model, 專門放 unique field_name
    topic_name = models.CharField(max_length=60,verbose_name=_('Topic Name'))                  # 應為存在的欄名說明(和翻譯檔相同)
    app_model= models.CharField(max_length=30,verbose_name=_('app model'))    # form設計為多選, 來自model-->django_content_type.app_label 及 model, memo性質
                                     # 主要是備註用在那些地方; 日後若技術成熟, 可用程式『自動搜尋』添加

    def __str__(self):
        return self.topic_name              # instance的值

    class Meta:
        managed = True
        verbose_name = _("UDC topic")
        verbose_name_plural = _("User-defined code's topic")



# 使用者自定義碼 : IT使用
class UserDefCode(DictionaryMixin, AuditMixin, models.Model):
    parent = models.ForeignKey('self',on_delete=models.CASCADE,blank=True, null=True, related_name=None,verbose_name=_("Tree's parent id"))  #多層定義碼時, 串連的依據
    topic_code = models.ForeignKey('TopicOfUdc',on_delete=models.CASCADE,related_name=None,verbose_name=_("UDC Topic"))
    udc = models.CharField(max_length=8, verbose_name=_("User Defined Code"))                                   #使用者自定義代碼
    desc1 = models.CharField(max_length=30, verbose_name=_("UDC Description1"))
    desc2 = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("UDC Description2"))

    shc1 = models.CharField(max_length=10, blank=True, null=True, verbose_name=_("Special Handling Code1"))                   #特殊處理代碼1  2021/08/17 二表增加
    shc1_desc = models.CharField(max_length=300, blank=True, null=True, verbose_name=_("Special Handling Code1 Description"))  #特殊處理說明1

    shc2 = models.CharField(max_length=10, blank=True, null=True, verbose_name=_("Special Handling Code2"))                   #特殊處理代碼2
    shc2_desc = models.CharField(max_length=300, blank=True, null=True, verbose_name=_("Special Handling Code2 Description"))  #特殊處理說明2

    shc3 = models.CharField(max_length=10, blank=True, null=True, verbose_name=_("Special Handling Code3"))                   #特殊處理代碼3
    shc3_desc = models.CharField(max_length=300, blank=True, null=True, verbose_name=_("Special Handling Code3 Description"))  #特殊處理說明3


    description = models.CharField(max_length=200, blank=True, null=True, verbose_name=_("Longer Description"))

    def __str__(self):
        return "{}".format(self.desc1)

    class Meta:
        managed = True
        ordering = ('topic_code','udc')
        unique_together = ('topic_code','udc')
        verbose_name = _("User-defined code")
        verbose_name_plural = _("User-defined codes")


#整批更新時使用
class UserDefCode_Update(models.Model):
    udc = models.CharField(max_length=8, unique=True,verbose_name=_("User Defined Code"))                                   #使用者自定義代碼
    desc1 = models.CharField(max_length=30, verbose_name=_("UDC Description1"))
    desc2 = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("UDC Description2"))
    description = models.CharField(max_length=200, blank=True, null=True, verbose_name=_("Longer Description"))

    class Meta:
        managed = True


# Registration Activity Rules:註冊活動規則(上一狀態\下一狀態) IT使用
class RegActRules(DictionaryMixin, AuditMixin,models.Model):
    # order_type = models.ForeignKey(UserDefCode, on_delete='CASCADE', related_name="order_type",\
    #                                limit_choices_to=Q(topic_code__startwith='order_type'),verbose_name="單據類型")
    order_type = models.CharField(default='', max_length=3 ,verbose_name="單據類型")     #設定在ProcessOptionsTxtDef:order_type,action='blank',不同的view會有不同的order_type
    # last_status = models.CharField(max_length=3, verbose_name="上一狀態碼")
    # next_status = models.CharField(max_length=3, verbose_name="下一狀態碼")
    last_status = models.CharField(max_length=3, verbose_name="上一狀態碼")
    next_status = models.CharField(max_length=3, verbose_name="下一狀態碼")
    status_desc = models.CharField(max_length=30, blank=True, null=True, verbose_name="狀態說明")
    write_ledger = models.BooleanField(default=False,verbose_name="是否寫入分類帳")  #狀態的來來往往,是否紀錄

    def __str__(self):
        return "{} {}".format(self.last_status,self.status_desc)

    class Meta:
        managed = True
        ordering = ('order_type','last_status',)
        unique_together = ('order_type','last_status',)
        verbose_name = _("Registration Activity Rule")
        verbose_name_plural = _("Registration Activity Rules")


# Processing Options Text  Definition: 處理選項文字定義(程式的預設處理規則) IT使用
class ProcessOptionsTxtDef(DictionaryMixin, AuditMixin, models.Model):
    blankDoc = 'blank'
    status_newDoc = 'new'
    status_submitDoc = 'submit'
    status_recallDoc = 'recall'
    status_returnDoc = 'return'
    status_voidDoc = 'void'
    status_closeDoc = 'closed'
    action_choices = [
        (blankDoc, '空白'),
        (status_newDoc,'新增'),
        (status_submitDoc,'送出'),
        (status_recallDoc,'收回'),
        (status_returnDoc,'退回'),
        (status_voidDoc, '作廢'),
        (status_closeDoc,'結案'),
    ]
    app_model = models.CharField(max_length=30,verbose_name=_('app model'))     # 這個處理選項的model的app
    view_code = models.CharField(max_length=30,verbose_name=_('View Code'))     # 應為存在的view, 要使用的處理選項的View
    view_name = models.CharField(max_length=60,verbose_name=_('View Name'))     # View用途說明
    model_class = models.CharField(max_length=30,verbose_name=_('model name'))  # 這個處理選項,要挑選的欄位的model
    topic_code = models.CharField(max_length=30,verbose_name=_('Topic Code'))   # 處理選項, 要判斷的櫚名
    topic_name = models.CharField(max_length=60,verbose_name=_('Topic Name'))   # 欄名說明

    po_code = models.CharField(max_length=120,verbose_name=_('Processing Options Code'))   # app_model.model_class.topic_code=po_code
                                                                                           # po_code會依topic_name欄位內容不同, 依其欄位的長度而定
                                                                                           # 所以要作處理選項的欄位, 其長度不可超過po_code的長度
    action = models.CharField(max_length=15,choices=action_choices,default=blankDoc,verbose_name=_('Action'))   #作為判斷同一個櫚位, 該取用那個po_code的依據


    def __str__(self):
        return "{} {} {} {}".format(self.view_code, self.view_name, self.action, self.po_code)

    class Meta:
        managed = True
        ordering = ('app_model','view_code','model_class','topic_code','po_code')
        unique_together = ('app_model','view_code','model_class','topic_code','po_code')    #一個view用到的model欄位,要設定的處理選項值...不可重覆,否則程式無法判斷要用那一個
        verbose_name = _("Processing Option")
        verbose_name_plural = _("Processing Options")


#紀錄刪除的動作( 因刪除就看不到資料了 )
class FileActionLedger(DictionaryMixin, AuditMixin, models.Model):
    app_name = models.CharField(default='', max_length=30, blank=True, null=True,verbose_name="應用程式")  # (User defined code-最長8碼)所屬公司
    model_name = models.CharField(default='', max_length=30, blank=True, null=True,verbose_name="檔案模組名")  # (User defined code-最長8碼)所屬公司
    pg_name = models.CharField(default='', max_length=30, blank=True, null=True, verbose_name="動作")
    act_btn = models.CharField(default='', max_length=30, blank=True, null=True, verbose_name="動作")
    btn_name = models.CharField(default='', max_length=30, blank=True, null=True, verbose_name="動作")
    url = models.URLField()
    formdata = models.CharField(default='',max_length=300, blank=True, null=True, verbose_name="表單的資料")
    # otherdata = models.CharField(default='',max_length=1024, blank=True, null=True, verbose_name="其他資料")
    otherdata = models.TextField(default='', blank=True, null=True, verbose_name="其他資料")


    def __str__(self):
        return "{} {}".format(self.app_name,self.model_name)

    class Meta:
        managed = True
        ordering = ('app_name','model_name',)
        verbose_name = _("File Action Memory Ledger")
        verbose_name_plural = _("File Action Memory Ledger")


#整批更新時使用
class GoogleLanguage(DictionaryMixin, AuditMixin, models.Model):
    lang_choices = [
        ('zh-TW', '中文(繁體)'),
        ('zh-CN','中文(簡體)'),
        ('en','英文'),
        ('vi','越南文'),
        ('id','印尼文'),
        ('ms','馬來文'),
        ('my','緬甸文'),
        ('km','高棉文'),
        ('hi','印度文'),
        ('th','泰文'),
        ('ja','日文'),
        ('ko','韓文'),
        ('ru','俄文'),
        ('de','德文'),
        ('fr','法文'),
        ('nl','荷蘭文'),
        ('pl','波蘭文'),
        ('fi','芬蘭文'),
        ('cs','捷克文'),
        ('es','西班牙文'),
        ('uk','烏克蘭文'),
        ('it','義大利文'),
        ('tr','土耳其文'),
        ('ar','阿拉伯文'),
    ]
    lang_code = models.CharField(primary_key=True,max_length=7, choices=lang_choices,verbose_name="語系")
    lang_desc = models.CharField(max_length=30,default="無",verbose_name="備註")

    def __str__(self):
        return "{} {}".format(self.lang_code,self.lang_desc)



#整批更新時使用
class DjangoLanguage(DictionaryMixin, AuditMixin, models.Model):
    lang_choices = [
        ('zh-TW', '中文(繁體)'),
        ('zh-CN','中文(簡體)'),
        ('en','英文'),
        ('vi','越南文'),
        ('id','印尼文'),
        ('ms','馬來文'),
        ('my','緬甸文'),
        ('km','高棉文'),
        ('hi','印度文'),
        ('th','泰文'),
        ('ja','日文'),
        ('ko','韓文'),
        ('ru','俄文'),
        ('de','德文'),
        ('fr','法文'),
        ('nl','荷蘭文'),
        ('pl','波蘭文'),
        ('fi','芬蘭文'),
        ('cs','捷克文'),
        ('es','西班牙文'),
        ('uk','烏克蘭文'),
        ('it','義大利文'),
        ('tr','土耳其文'),
        ('ar','阿拉伯文'),
    ]
    lang_code = models.CharField(primary_key=True,max_length=7, choices=lang_choices,verbose_name="語系")
    lang_desc = models.CharField(max_length=30,default="無",verbose_name="備註")

    def __str__(self):
        return "{} {}".format(self.lang_code,self.lang_desc)


# 簽名欄位定義_版本
class ReportInformation(DictionaryMixin, AuditMixin, models.Model):
    app_model = models.CharField(max_length=30,verbose_name='app model')    # 這個處理選項的model的app
    view_code = models.CharField(max_length=30,verbose_name='View Code')    # 應為存在的view, 要使用的處理選項的View
    view_name = models.CharField(max_length=60,verbose_name='View Name')    # View用途說明
    report_code = models.CharField(max_length=30,verbose_name='報表代碼')     # View用途說明app_model+view_code+自取名字
    report_name = models.CharField(max_length=100,verbose_name='報表名稱')    #
    report_version = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)],verbose_name="簽名流程版本")
    page_size = [
        ('A3', 'A3  w29.7*h42'),
        ('A4', 'A4  w21*h29.7'),
        ('A5', 'A5  w14.8*h21'),
        ('B4', 'B4  w25.7*h36.4'),
        ('B5', 'B5  w18.2*h25.7'),
        ('Letter', 'Letter  w21.59*h27.94'),
    ]
    report_size = models.CharField(max_length=10,blank=True,null=True,choices=page_size,verbose_name=' 總張選擇')
    orientation_choice= [
        ('P', '直式 Portrait'),
        ('L', '橫式 Landscape'),
    ]
    report_orientation = models.CharField(max_length=1,choices=orientation_choice,blank=True,null=True, verbose_name='方向 橫式/直式')
    report_title = models.CharField(max_length=100,blank=True,null=True, verbose_name='報表抬頭')
    enable_date = models.DateField(default=now,blank=True,null=True,verbose_name="啟用日期")
    disable_date = models.DateField(blank=True,null=True, verbose_name="失效日期")
    description = models.CharField(max_length=100, blank=True, null=True, verbose_name="更版說明")

    def __str__(self):
        return "{} {} {}".format(self.report_code,self.report_name,self.report_version)

    class Meta:
        managed = True
        ordering = ('report_code','report_version')
        unique_together = ('report_code','report_version')
        verbose_name = "報表版本"
        verbose_name_plural = "報表版本"


# 簽名欄位定義
class ReportSign(DictionaryMixin, AuditMixin, models.Model):
    report_info = models.ForeignKey(ReportInformation,related_name='report_sign',on_delete='CASCADE',null=True,verbose_name="報表版本")
    order_number = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)],verbose_name="簽核順序")
    sign_title = models.CharField(max_length=20, null=True, blank=True,verbose_name="簽核抬頭")
    sign_space = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)],verbose_name="簽名寬度")

    def __str__(self):
        return "{} {} {}".format(self.report_info,self.order_number,self.sign_title)

    class Meta:
        managed = True
        ordering = ('report_info','order_number')
        unique_together = ('report_info','order_number')
        verbose_name = "報表簽核流程順序"
        verbose_name_plural = "報表簽核流程順序"



# 簽名欄位定義外國語言
class ReportSignForeign(DictionaryMixin, AuditMixin, models.Model):
    report_sign = models.ForeignKey(ReportSign,on_delete=models.CASCADE,verbose_name="簽名流程")
    lang_code = models.CharField(max_length=7,choices=choice_language,verbose_name="語系")
    sign_title = models.CharField(max_length=60, null=True, blank=True,verbose_name="簽核抬頭")
    sign_space = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)],verbose_name="簽名寬度")

    def __str__(self):
        return "{} {} {}".format(self.report_sign,self.lang_code,self.sign_title)


    class Meta:
        managed = True
        ordering = ('report_sign','lang_code')
        unique_together = ('report_sign','lang_code')
        verbose_name = "報表簽核流程順序_外國語言"
        verbose_name_plural = "報表簽核流程順序_外國語言"
