from django.db import models
from datetime import date
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.postgres.fields import IntegerRangeField
from django.utils.translation import gettext_lazy as _

import os
from django.conf import settings

from common.mixins import DictionaryMixin, AuditMixin
from common.models import UserDefCode,RegActRules
from system.models import Factory
from django.utils import timezone
from jsignature.fields import JSignatureField


current_tz = timezone.get_current_timezone()
now = timezone.now().astimezone(current_tz).strftime('%Y-%m-%d')


# 簽名檔
class SignatureModel(models.Model):
    signature = JSignatureField()


class EmployeeInfoEasy(DictionaryMixin, AuditMixin, models.Model):
    work_code = models.CharField(primary_key=True,max_length=8, blank=True, verbose_name="工號")  # 工號
    chi_name = models.CharField(max_length=20, blank=True, null=True, verbose_name="姓名")     # 中文姓名　

    email = models.EmailField(blank=True, null=True, verbose_name="E-mail")  #個人的email(主管評核完，要寄出通知的帳號)　

    corp = models.ForeignKey(UserDefCode, on_delete='CASCADE', limit_choices_to={'topic_code':'corp_id'},
                                related_name="corp_id_1",blank=True, null=True,
                                verbose_name="備用欄位(改用factory取代)")  # XX (User defined code-最長8碼)所屬公司
    factory = models.ForeignKey(Factory, on_delete='CASCADE', related_name="factory",blank=True, null=True,
                                verbose_name="公司")  # 所屬公司
    factory_area = models.ForeignKey(UserDefCode, on_delete='CASCADE', limit_choices_to={'topic_code':'factory_area_id'},
                                related_name="factory_area_id",blank=True, null=True,
                                verbose_name="廠區")  # (User defined code-最長8碼)所屬廠區 2021/07/02 add
    dept_flevel = models.ForeignKey(UserDefCode, on_delete='CASCADE', limit_choices_to={'topic_code':'dept_flevel_id'},
                                related_name="dept_flevel_id",blank=True, null=True,
                                verbose_name="一級部門")  # (User defined code-最長8碼)所屬一級部門 2021/07/02 add
    dept = models.ForeignKey(UserDefCode, on_delete='CASCADE', limit_choices_to={'topic_code':'dept_id'},
                                related_name="dept_id_1",blank=True, null=True,
                                verbose_name="部門別")  # (User defined code-最長8碼)所屬部門
    dept_desc = models.ForeignKey(UserDefCode, on_delete='CASCADE', limit_choices_to={'topic_code':'dept_desc_id'},
                                related_name="dept_desc_id",blank=True, null=True,
                                verbose_name="部門全稱")  # (User defined code-最長8碼)部門全稱 2021/07/02 add
    pos = models.ForeignKey(UserDefCode, on_delete='CASCADE', limit_choices_to ={'topic_code':'pos_id'},
                               related_name="pos_it_1",blank=True, null=True,
                               verbose_name="職稱(位)")  # (User defined code-最長8碼)主要職位
    director = models.ForeignKey('self',on_delete=models.SET_NULL,to_field=('work_code'),
                                    related_name="director_id_1",blank=True, null=True,
                                    verbose_name="評核主管")  # 評核主管
    # director = models.CharField(max_length=8,blank=True, null=True,verbose_name="評核主管")  # 評核主管
    direct_supv = models.ForeignKey('self',on_delete=models.SET_NULL,to_field=('work_code'), # 直接主管
                                    related_name="director_id_2",blank=True, null=True,
                                    verbose_name="直接主管")  # 直接主管 2021/07/02 add
    # 主管(先手key姓名, 到時後, 再依"工號"..存工號)
    arrival_date = models.DateField(default=None,blank=True, null=True,verbose_name="到職日")  # 到職日期
    resign_date = models.DateField(default=None,blank=True, null=True,verbose_name="離職日")  # 離職日期
    trans_date = models.DateField(default=None,blank=True, null=True,verbose_name="異動日")  # 異動日期     2021/08/30 add app:skill_pdca

    trans_type_choices = (
        ('轉正', '轉正'),
        ('復職','復職') ,
        ('調職','調職') ,
        ('其他','其他'),
    )
    trans_type = models.CharField(default=None,max_length=10, choices=trans_type_choices,blank=True, null=True, verbose_name="異動類別")     # 異動類別

    rank = models.ForeignKey(UserDefCode, on_delete='CASCADE', limit_choices_to ={'topic_code':'rank_id'},
                               related_name="rank_id",blank=True, null=True,
                               verbose_name="職等")  # (User defined code-最長8碼)KPI/BSC的評核依據
    nat = models.ForeignKey(UserDefCode, on_delete='CASCADE', limit_choices_to ={'topic_code':'nat_id'},
                               related_name="nat_id",blank=True, null=True,
                               verbose_name="國籍")  # (User defined code-最長8碼) 不同國籍(國外),奬金折數不同
    labor_type = models.ForeignKey(UserDefCode, on_delete='CASCADE', limit_choices_to ={'topic_code':'labor_type_id'},
                               related_name="labor_type_id",blank=True, null=True,
                               verbose_name="直接/間接")  # (User defined code-最長8碼)
    bonus_type = models.ForeignKey(UserDefCode, on_delete='CASCADE', limit_choices_to ={'topic_code':'bonus_type_id'},
                               related_name="bonus_type_id",blank=True, null=True,
                               verbose_name="獎金型態")  # (User defined code-最長8碼)
    bonus_factor = models.ForeignKey(UserDefCode, on_delete='CASCADE', limit_choices_to ={'topic_code':'bonus_factor_id'},
                               related_name="bonus_factor_id",blank=True, null=True,
                               verbose_name="獎金點數")  # (User defined code-最長8碼) 每個人的獎金係數不同
    eval_class = models.ForeignKey(UserDefCode, on_delete='CASCADE', limit_choices_to ={'topic_code':'eval_class_id'},
                               related_name="eval_class_id",blank=True, null=True,
                               verbose_name="BSC/KPI")  # (User defined code-最長8碼) 評核BSC/KPI的依據

    service_status = models.ForeignKey(UserDefCode, on_delete='CASCADE', limit_choices_to ={'topic_code':'service_status_id'},
                               related_name="service_status_id",blank=True, null=True,
                               verbose_name="服務狀態")  # (User defined code-最長8碼)正式/試用員工  2021/07/02 add

    kpi_diy = models.BooleanField(verbose_name='自評')       # 2021/09/17增加( 預設=True可自評,False不可自評)  app:kpi  KPI自評 )
    pdca_agent = models.BooleanField(default=False,verbose_name='代填')    # 2022/06/08增加( 預設=False-"工作事項明細表"自行填寫,True:由主管代為填寫 )
    dept_description = models.CharField(default='',max_length=300, blank=True, null=True, verbose_name="部門全稱")
    # skill_diy = models.BooleanField(verbose_name='自盤')          #XX 2021/09/17增加(預設=False不可自己盤點,True可自盤) app:skill_pdca

    urrf = models.CharField(default='',max_length=25, blank=True, null=True, verbose_name="User Reserved Reference")
    urrf1 = models.CharField(default='',max_length=50, blank=True, null=True, verbose_name="User Reserved Reference1")
    urrf2 = models.CharField(default='',max_length=50, blank=True, null=True, verbose_name="User Reserved Reference2")



    def __str__(self):
        return '%s %s' % (self.work_code,self.chi_name)  # instance的值

    def __unicode__(self):
        return '%s %s' % (self.work_code,self.chi_name)

    class Meta:
        managed = True
        # app_label = 'kpi'
        # db_table = 'EmployeeInfo'　　　　　　　未自定db_table, 會以 ( app名稱+"_" )為前綴
        ordering = ('work_code',)
        verbose_name = "員工基本資料"
        verbose_name_plural = "員工基本資料"


class EmployeeInfoEasy_update(models.Model):
    #以下欄位,為HR比較正確的欄位,先整理好, 幫人資更新一次, 再讓其做EXCEL匯出整理,整理服務狀態時, 記得看"離職日"
    work_code = models.CharField(primary_key=True,max_length=8, blank=True, verbose_name="工號")  # 工號
    dept_description = models.CharField(default='',max_length=300, blank=True, null=True, verbose_name="Department full name")
    factory_area = models.ForeignKey(UserDefCode, on_delete='CASCADE', limit_choices_to={'topic_code':'factory_area_id'},
                                related_name="EmployeeInfoEasy_update1",blank=True, null=True,
                                verbose_name="廠區")
    service_status = models.ForeignKey(UserDefCode, on_delete='CASCADE', limit_choices_to ={'topic_code':'service_status_id'},
                               related_name="EmployeeInfoEasy_update2",blank=True, null=True,
                               verbose_name="服務狀態")  # (User defined code-最長8碼)正式/試用員工/離職員工
    resign_date = models.DateField(default=None, blank=True, null=True, verbose_name="離職日")  # 離職日期


#本檔做為匯入後,用SQL更新 EmployeeInfoEasy.work_code_tw 使用；本質上，無任何做用
class WorkcodeMapping(DictionaryMixin, AuditMixin, models.Model):
    factory = models.ForeignKey(Factory, on_delete='CASCADE', related_name="workcode_map",blank=True, null=True,
                                verbose_name="公司")  # 所屬公司
    work_code = models.CharField(max_length=12,blank=True, null=True,verbose_name="工號")          #工號
    work_code_x = models.ForeignKey(EmployeeInfoEasy,on_delete=models.CASCADE,related_name="work_code_x", blank=True, null=True,verbose_name="其他工號")  #台灣工號/大陸工號/他廠工號
    chi_name = models.CharField(max_length=20, blank=True, null=True, verbose_name="姓名")               # 中文姓名　
    alias_name = models.CharField(max_length=30, blank=True, null=True, verbose_name="別名")             # 別名　
    factory_area = models.ForeignKey(UserDefCode, on_delete='CASCADE', limit_choices_to={'topic_code':'factory_area_id'},
                                related_name="workcode_map",blank=True, null=True,
                                verbose_name="廠區")  #
    class Meta:
        managed = True
        ordering = ('work_code','work_code_x')
        unique_together = ('work_code','work_code_x')
        verbose_name = "海外員工vs台灣工號對照表"
        verbose_name_plural = "海外員工vs台灣工號對照表"


class DeptSupervisor(DictionaryMixin, AuditMixin, models.Model):
    factory = models.ForeignKey(Factory, on_delete='CASCADE', related_name="dept_supervisor",blank=True, null=True,
                                verbose_name="公司")  # 所屬公司
    dept = models.ForeignKey(UserDefCode, on_delete='CASCADE', limit_choices_to={'topic_code': 'dept_id'},
                             related_name="dept_hr1", primary_key=True,verbose_name="部門")              #(User defined code-最長8碼)所屬部門
    dept_upper = models.ForeignKey(UserDefCode, on_delete='CASCADE', limit_choices_to={'topic_code': 'dept_id'},
                             related_name="dept_hr2", blank=True, null=True, verbose_name="上級部門")        #(User defined code-最長8碼)所屬部門
    dept_flevel = models.ForeignKey(UserDefCode, on_delete='CASCADE', limit_choices_to={'topic_code':'dept_id'},
                                related_name="dept_hr3",blank=True, null=True, verbose_name="一級部門")  #(User defined code-最長8碼)所屬一級部門 2021/07/02 add
    dept_supervisor = models.ForeignKey(EmployeeInfoEasy,on_delete=models.CASCADE, null=True,verbose_name="工號")  #工號
    dept_description = models.CharField(default='',max_length=300, blank=True, null=True, verbose_name="部門全稱")
    urrf = models.CharField(default='',max_length=25, blank=True, null=True, verbose_name="User Reserved Reference")
    urrf1 = models.CharField(default='',max_length=50, blank=True, null=True, verbose_name="User Reserved Reference1")
    urrf2 = models.CharField(default='',max_length=50, blank=True, null=True, verbose_name="User Reserved Reference2")

    class Meta:
        managed = True
        verbose_name = "部門主管對照表"
        verbose_name_plural = "部門主管對照表"


class MetricsSetup(DictionaryMixin, AuditMixin, models.Model):
    metrics_id = models.AutoField(primary_key=True, verbose_name="衡量指標")  # 衡量指標
    # id = models.AutoField(primary_key=True, verbose_name="衡量指標")  # 衡量指標
    work_code = models.ForeignKey(EmployeeInfoEasy,on_delete=models.CASCADE,
                                  null=True,verbose_name="工號")     #工號
    # 工號(共同衡量類型的工號為,中良工業:1000-000,中良江西:2000-000)
    metrics_type = models.ForeignKey(UserDefCode, on_delete='CASCADE', limit_choices_to={'topic_code':'metrics_type'},
                                related_name="metrics_type_1",blank=True, null=True,
                                verbose_name="指標類型")  # (User defined code-最長8碼)衡量指標類型
    score_type_choices = (
        ('A','自評實績') ,
        ('B','主管評核') ,
        ('C','匯入實績'),
    )
    score_type = models.CharField(max_length=1, choices=score_type_choices,verbose_name="評核方式")    #2021/04/07增加(評核方式)
    order_number = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),MaxValueValidator(99)],verbose_name="順序")
    order_item  = models.PositiveSmallIntegerField(default=0,validators=[MinValueValidator(0), MaxValueValidator(9)],verbose_name="順序細項")
    date_yyyy=models.PositiveSmallIntegerField(validators=[MinValueValidator(2020), MaxValueValidator(2100)],verbose_name="年度")  # 西元年4位
    date_mm = models.PositiveSmallIntegerField(default=0,validators=[MinValueValidator(0), MaxValueValidator(12)],verbose_name="月份")  # 月份2位

    metrics_content = models.CharField(max_length=220,blank=True, null=True, verbose_name="衡量指標")        # 衡量內容

    metrics_txt1 = models.CharField(max_length=100,blank=True, null=True, verbose_name="衡量指標")
    metrics_number = models.DecimalField(max_digits=11,decimal_places=2,null=True,verbose_name="(一定要有數字)")   #2021/10/22修改
    metrics_txt2 = models.CharField(max_length=100,blank=True, null=True, verbose_name="衡量指標")

    unit_Mcalc = models.ForeignKey(UserDefCode, on_delete='CASCADE', limit_choices_to={'topic_code':'unit_Mcalc'},
                                related_name="unit_Mcalc",blank=True, null=True,
                                verbose_name="單位")
    asc_desc_choices = (
        ('A','遞增') ,
        ('D','遞減'),
    )
    asc_desc = models.CharField(max_length=1, choices=asc_desc_choices,verbose_name="遞增/遞減")    #2021/04/06增加(計算方式的遞增/遞減)
    auto_alloc = models.BooleanField(blank=True, null=True,verbose_name='自動分配')                 #2021/04/06增加(計算方式是否自動分配)
    alloc_range = models.IntegerField(blank=True, null=True, verbose_name="範圍")                  #2021/04/06增加(計算方式自動分配範圍)
    allocation = models.DecimalField(max_digits=12,decimal_places=2,null=True,verbose_name="最高配分")    #2021/10/22 修改
    low_limit = models.DecimalField(max_digits=12,decimal_places=2,null=True,verbose_name="最低配分")   #2021/10/22 修改
    ef_date = models.DateField(blank=True, null=True,verbose_name="生效日期")                      # 生效日期
    exp_date = models.DateField(blank=True, null=True,verbose_name="生效日期")                     # 失效日期
    urrf = models.CharField(default='',max_length=25, blank=True, null=True, verbose_name="User Reserved Reference")
    urrf1 = models.CharField(default='',max_length=50, blank=True, null=True, verbose_name="User Reserved Reference1")
    urrf2 = models.CharField(max_length=50, blank=True, null=True, verbose_name="User Reserved Reference2")

    asc_desc_score = models.CharField(max_length=1, choices=asc_desc_choices,verbose_name="遞增/遞減")    #2021/06/21增加(得分的遞增/遞減)
    # 2021/6/21增加(衡量指標和計算方式,是否設計完成, 確認時會做相關檢查, 關帳時未確認者將列出來, 不可關帳, 已確認者, 不可修改)
    # confirmed = models.BooleanField(default=False,blank=True, null=True, verbose_name='確認')  # 2021/6/21增加(衡量指標和計算方式,是否設計完成, 確認時會做相關檢查, 關帳時未確認者將列出來, 不可關帳)
    confirmed = models.CharField(default='',max_length=1,blank=True, null=True, verbose_name='確認')  # 2021/6/21增加(衡量指標和計算方式,是否設計完成, 確認時會做相關檢查, 關帳時未確認者將列出來, 不可關帳)


    def __str__(self):
        return '%s %s' % (self.work_code,self.metrics_content)

    def __unicode__(self):
        return '%s %s' % (self.work_code,self.metrics_content)


    class Meta:
        managed = True
        ordering = ('work_code','date_yyyy','date_mm','order_number','order_item')
        unique_together = ('work_code','date_yyyy','date_mm','order_number','order_item')
        verbose_name = "指標設定"
        verbose_name_plural = "指標設定"



class MetricsCalc(DictionaryMixin, AuditMixin, models.Model):
    # metrics = models.ForeignKey('MetricsSetup',related_name='metrics_calc',on_delete='CASCADE',null=True,verbose_name="衡量指標")
    metrics = models.ForeignKey('MetricsSetup',related_name='metrics_calc',on_delete='PROTECT',null=True,verbose_name="衡量指標")
    order_number = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)],verbose_name="順序")
    calc_content = models.TextField(verbose_name="計算方式")
    lower_limit = models.DecimalField(max_digits=11,decimal_places=2,null=True,verbose_name="下限(>=)")    #2021/10/22 修改成小數1-->2位,最大位數5-->15
    upper_limit = models.DecimalField(max_digits=11,decimal_places=2,null=True,verbose_name="上限(<)")     #2021/10/22 修改成小數1-->2位,最大位數5-->15
    score = models.DecimalField(max_digits=12,decimal_places=2,null=True,verbose_name="得分")  # 配分比重   0~32767  2021/10/22修改
    # 最高不可超越MetricSetup.allocation
    ef_date = models.DateField(blank=True, null=True,verbose_name="生效日")  # 生效日期
    exp_date = models.DateField(blank=True, null=True,verbose_name="失效日")      # 失效日期

    def __str__(self):
        return "{} {} {}".format(self.metrics,self.calc_content,self.score)  # instance的值

    def __unicode__(self):
        return "{} {} {}".format(self.metrics,self.calc_content,self.score)  # instance的值

    class Meta:
        managed = True
        ordering = ('metrics','order_number',)
        unique_together = ('metrics', 'order_number',)
        verbose_name = "指標計算方式"
        verbose_name_plural = "指標計算方式"



# 評核的年月
class WorkingYM(DictionaryMixin, AuditMixin, models.Model):
    date_yyyy=models.PositiveSmallIntegerField(validators=[MinValueValidator(2020), MaxValueValidator(2100)],verbose_name="年度")  # 西元年4位
    date_mm = models.PositiveSmallIntegerField(default=0,validators=[MinValueValidator(0), MaxValueValidator(12)],verbose_name="月份")  # 月份2位
    before_lastdate = models.PositiveSmallIntegerField(default=0,verbose_name="月底往前推?天")
    diy_date = models.DateField(default=None,blank=True, null=True,verbose_name="自評期限")  # 異動日期     2021/09/24 增加
    err_release =  models.BooleanField(default=False,verbose_name='檢核有錯誤,是否放行')            #2021/11/25加入

    class Meta:
        managed = True
        unique_together = ('date_yyyy', 'date_mm',)
        verbose_name = "作業年月"
        verbose_name_plural = "作業年月"


class ScoreSheet(DictionaryMixin, AuditMixin, models.Model):
    #                             related_name="order_type_ScoreSheet",verbose_name="單據類型")  # (User defined code-最長8碼)單據別(BSC/KPI)
    order_type = models.CharField(max_length=3, verbose_name="KPI")
    metrics = models.ForeignKey('MetricsSetup',primary_key=True, related_name='score_sheet', on_delete=models.CASCADE, verbose_name="衡量指標")
    calc_content = models.TextField(blank=True, null=True,verbose_name="計算方式")
    metrics_calc = models.DecimalField(max_digits=11,decimal_places=2,null=True,verbose_name="得分")           # 初評 (單選) (記錄初評時內容)
    actual_score = models.DecimalField(max_digits=11,decimal_places=2,null=True,verbose_name="自評實績")   #2021/10/22修改

    last_status = models.ForeignKey(RegActRules, on_delete='CASCADE',
                                related_name="score_sheet",blank=True, null=True,
                                verbose_name="最後狀態"        )
    check = models.BooleanField(verbose_name='人資已抽檢', blank=True, null=True)   #2021/3/31增加
    # rsn_code = models.ForeignKey(UserDefCode, on_delete='CASCADE', limit_choices_to={'topic_code':'rsn_code'},
    #                             related_name="rsn_code",blank=True, null=True,
    #                             verbose_name="退回原因")                            #(User defined code-最長8碼)
    # rsn_desc = models.TextField(blank=True, null=True,verbose_name="退回說明")

    # 2021/08/03 add : 將自評儲存起來,可以和『主管審核』做比對( 備而不用 )
    bu_calc_content = models.TextField(blank=True, null=True,verbose_name="計算方式.自評備份")
    bu_actual_score = models.DecimalField(max_digits=11,decimal_places=2,null=True,verbose_name="自評實績.自評備份")       #2021/10/22修改
    bu_metrics_calc = models.DecimalField(max_digits=12,decimal_places=2,null=True,verbose_name="得分.自評備份")          #2021/10/22修改


    def __str__(self):
        return "{} {}".format(self.metrics,self.metrics_calc)  # instance的值

    def __unicode__(self):
        return "{} {}".format(self.metrics, self.metrics_calc)  # instance的值

    class Meta:
        managed = True
        verbose_name = "員工評核表"
        verbose_name_plural = "員工評核表"


def reports_path():
    return os.path.join(settings.MEDIA_ROOT,'/media-files/reports/pdf/')

class ScoreStatus(DictionaryMixin, AuditMixin, models.Model):
    order_type = models.CharField(max_length=3, blank=True, null=True,verbose_name="KPI/BSC")
    # work_code = models.CharField(max_length=8, blank=True, verbose_name="工號")    #工號
    work_code = models.ForeignKey(EmployeeInfoEasy,on_delete=models.CASCADE,related_name="ScoreStatus_work_code",
                                  null=True,verbose_name="員工")     #工號
    #不由work_code連接,是因為要記錄當下的『評核主管』
    #若由work_code連接,若多年以後,評核主管變更,會跑出當下的評核主管,那就不準確了
    # director = models.CharField(max_length=8, blank=True, verbose_name="評核主管")  #當下的評核主管
    director = models.ForeignKey(EmployeeInfoEasy,on_delete=models.CASCADE,related_name="ScoreStatus_director",
                                  null=True,verbose_name="評核主管")     #
    date_yyyy = models.PositiveSmallIntegerField(verbose_name="年度")    # 西元年4位
    quarter = models.PositiveSmallIntegerField(verbose_name="季")       # 季1位
    report_name = models.FilePathField(default='',path=reports_path,verbose_name="報表名稱")
    report_url = models.URLField(verbose_name="報表網址")

    #KPI+YEAR(4位)+MONTH(2位)+DAY(2位)+id(取4位)
    bpm_number = models.CharField(default='',blank=True,max_length=15, verbose_name="BPM單號")
    bpm_status_choices = (
        ('1_draft','草稿') ,
        ('2_pending','待簽名') ,
        ('3_inreview','簽名中'),
        ('4_signed','簽名完畢'),
    )
    # 文件建立:draft
    # bpm送出:pending
    # 員工已開啟:inreview
    # 簽名送出:signed

    bpm_status = models.CharField(default='', max_length=12, choices=bpm_status_choices, blank=True, null=True,
                                  verbose_name="BPM狀態")

    def __str__(self):
        return "{} {} {} {}".format(self.order_type,self.work_code,self.date_yyyy,self.quarter)  # instance的值

    def __unicode__(self):
        return "{} {} {} {}".format(self.order_type,self.work_code,self.date_yyyy,self.quarter)  # instance的值

    class Meta:
        managed = True
        ordering = ('order_type','work_code', 'date_yyyy', 'quarter')
        unique_together = ('order_type','work_code', 'date_yyyy', 'quarter')
        verbose_name = "員工評核表狀態"
        verbose_name_plural = "員工評核表狀態"



class ReportQuarter(DictionaryMixin, AuditMixin, models.Model):
    score_status = models.ForeignKey('ScoreStatus',on_delete=models.CASCADE, verbose_name="BPM簽核")
    order_type = models.CharField(max_length=3, verbose_name="KPI/BSC")
    work_code = models.CharField(max_length=8, blank=True, null=True, verbose_name="工號")  #工號
    chi_name = models.CharField(max_length=20, blank=True, null=True, verbose_name="姓名")        #中文姓名　
    dept = models.CharField(max_length=30, blank=True, null=True, verbose_name="部門別")          #部門 : 寫中文不寫代碼
    metrics_type = models.CharField(max_length=10,blank=True, null=True,verbose_name="指標類型")                         #個人指標/共同指標 : 寫中文不寫代碼
    metrics_id = models.IntegerField(verbose_name="衡量指標")
    score_type = models.CharField(max_length=10, blank=True, null=True,verbose_name="評核方式")                          #自評實績/主管評核/匯入實績
    order_number = models.PositiveSmallIntegerField(verbose_name="順序")
    order_item  = models.PositiveSmallIntegerField(verbose_name="順序細項")

    metrics_content = models.CharField(max_length=220,blank=True, null=True, verbose_name="衡量指標")


    date_yyyy=models.PositiveSmallIntegerField(verbose_name="年度")  # 西元年4位      xxx
    quarter = models.PositiveSmallIntegerField(verbose_name="季")     #季1位         xxx
    metrics_calc_avg = models.DecimalField(max_digits=12, decimal_places=2, null=True, verbose_name="總得分_平均")

    #date_mm1  月份1
    date_mm1 = models.PositiveSmallIntegerField(verbose_name="月份1")  #月份2位
    allocation1 = models.DecimalField(max_digits=11,decimal_places=2,verbose_name="配分")
    allocation1_tot = models.DecimalField(max_digits=12,decimal_places=2,verbose_name="總配分")       #2021/10/22修改
    order_number1 = models.PositiveSmallIntegerField(verbose_name="計算方式順序")
    calc_content1 = models.CharField(max_length=600,blank=True, null=True,verbose_name="計算方式1")
    actual_score1 = models.DecimalField(max_digits=11,decimal_places=2,verbose_name="實績2")
    metrics_calc1 = models.DecimalField(max_digits=12,decimal_places=2,verbose_name="得分1")
    metrics_calc1_tot = models.DecimalField(max_digits=12,decimal_places=2,verbose_name="總得分1")

    # date_mm2  月份2
    date_mm2 = models.PositiveSmallIntegerField(verbose_name="月份2")  #月份2位
    allocation2 = models.DecimalField(max_digits=12,decimal_places=2,verbose_name="配分")
    allocation2_tot = models.DecimalField(max_digits=12,decimal_places=2,verbose_name="總配分")
    order_number2 = models.PositiveSmallIntegerField(verbose_name="計算方式順序")
    calc_content2 = models.CharField(max_length=600,blank=True, null=True,verbose_name="計算方式2")
    actual_score2 = models.DecimalField(max_digits=11,decimal_places=2,verbose_name="實績2")
    metrics_calc2 = models.DecimalField(max_digits=12,decimal_places=2,verbose_name="得分2")
    metrics_calc2_tot = models.DecimalField(max_digits=12,decimal_places=2,verbose_name="總得分2")

    # date_mm3  月份3
    date_mm3 = models.PositiveSmallIntegerField(verbose_name="月份3")  #月份2位
    allocation3 = models.DecimalField(max_digits=12,decimal_places=2,verbose_name="配分")
    allocation3_tot = models.DecimalField(max_digits=12,decimal_places=2,verbose_name="總配分")
    order_number3 = models.PositiveSmallIntegerField(verbose_name="計算方式順序")
    calc_content3 = models.CharField(max_length=600,blank=True, null=True,verbose_name="計算方式3")
    actual_score3 = models.DecimalField(max_digits=11,decimal_places=2,verbose_name="實績3")
    metrics_calc3 = models.DecimalField(max_digits=12,decimal_places=2,verbose_name="得分3")
    metrics_calc3_tot = models.DecimalField(max_digits=12,decimal_places=2,verbose_name="總得分3")

    def __str__(self):
        return "{} {}".format(self.metrics_id,self.metrics_content)  # instance的值

    def __unicode__(self):
        return "{} {}".format(self.metrics_id, self.metrics_content)  # instance的值

    class Meta:
        managed = True
        ordering = ('order_type','work_code', 'date_yyyy', 'quarter','order_number','order_item')
        # unique_together = ('order_type','work_code', 'date_yyyy', 'quarter','metrics_id','order_number','order_item','score_status')
        verbose_name = "員工評核表"
        verbose_name_plural = "員工評核表"


'''
class EeAttendDetails(DictionaryMixin, AuditMixin, models.Model):
    work_code = models.ForeignKey(EmployeeInfoEasy,on_delete=models.CASCADE,related_name="ee_attend_details",
                                  null=True,verbose_name="員工工號")     #工號
    # metrics = models.ForeignKey('MetricsSetup',on_delete=models.CASCADE,null=True,related_name="ee_attend_details",verbose_name="衡量指標")  # 衡量指標ID(內容為 "出勤")
    attend_date = models.DateField(max_length=8,verbose_name="出勤日期")                  #出勤日期

    attend_type_01 = models.CharField(default="事假", max_length=20,null=True,blank=True,verbose_name="")           #出勤類型
    attend_unit_01 = models.CharField(default="天", max_length=5,null=True,blank=True ,verbose_name="天數")    #出勤單位
    attend_value_01 = models.DecimalField( max_digits=12,decimal_places=2,null=True,blank=True,verbose_name="天數")

    attend_type_02 = models.CharField(default="病假",max_length=20,null=True,blank=True,verbose_name="")           #出勤類型
    attend_unit_02 = models.CharField(default="天", max_length=5,null=True,blank=True ,verbose_name="天數")    #出勤單位
    attend_value_02 = models.DecimalField( max_digits=12,decimal_places=2,null=True,blank=True,verbose_name="天數")

    attend_type_03 = models.CharField(default="曠工", max_length=20,null=True,blank=True, verbose_name="")  # 出勤類型
    attend_unit_03 = models.CharField(default="天", max_length=5,null=True,blank=True  , verbose_name="天數")  # 出勤單位
    attend_value_03 = models.DecimalField( max_digits=12,decimal_places=2,null=True,blank=True,verbose_name="天數")  # 遲到 / 次

    attend_type_04 = models.CharField(default="遲到", max_length=20,null=True,blank=True, verbose_name="")  # 出勤類型
    attend_unit_04 = models.CharField(default="次", max_length=5,null=True,blank=True  , verbose_name="次數")  # 出勤單位
    attend_value_04 = models.DecimalField( max_digits=12,decimal_places=2,null=True,blank=True,verbose_name="次數")  # 遲到 / 次

    attend_type_05 = models.CharField(default="早退", max_length=20,null=True,blank=True,verbose_name="")           #出勤類型
    attend_unit_05 = models.CharField(default="次", max_length=5,null=True,blank=True ,verbose_name="次數")    #出勤單位
    attend_value_05 = models.DecimalField( max_digits=12,decimal_places=2,null=True,blank=True,verbose_name="次數")

    attend_type_06 = models.CharField(default="申誡", max_length=20,null=True,blank=True,verbose_name="")           #出勤類型
    attend_unit_06 = models.CharField(default="次", max_length=5,null=True,blank=True ,verbose_name="次數")    #出勤單位
    attend_value_06 = models.DecimalField( max_digits=12,decimal_places=2,null=True,blank=True,verbose_name="次數")

    attend_type_07 = models.CharField(default="小過", max_length=20,null=True,blank=True, verbose_name="")  # 出勤類型
    attend_unit_07 = models.CharField(default="次", max_length=5,null=True,blank=True  , verbose_name="次數")  # 出勤單位
    attend_value_07 = models.DecimalField( max_digits=12,decimal_places=2,null=True,blank=True,verbose_name="次數")

    attend_type_08 = models.CharField(default="大過", max_length=20,null=True,blank=True, verbose_name="")  # 出勤類型
    attend_unit_08 = models.CharField(default="次", max_length=5,null=True,blank=True  , verbose_name="次數")  # 出勤單位
    attend_value_08 = models.DecimalField( max_digits=12,decimal_places=2,null=True,blank=True,verbose_name="次數")

    attend_type_09 = models.CharField(default="嘉獎", max_length=20,null=True,blank=True, verbose_name="")  # 出勤類型
    attend_unit_09 = models.CharField(default="次", max_length=5,null=True,blank=True  , verbose_name="次數")  # 出勤單位
    attend_value_09 = models.DecimalField( max_digits=12,decimal_places=2,null=True,blank=True,verbose_name="次數")

    attend_type_10 = models.CharField(default="小功", max_length=20,null=True,blank=True, verbose_name="")  # 出勤類型
    attend_unit_10 = models.CharField(default="次", max_length=5,null=True,blank=True  , verbose_name="次數")  # 出勤單位
    attend_value_10 = models.DecimalField(max_digits=12,decimal_places=2,null=True,blank=True,verbose_name="次數")

    attend_type_11 = models.CharField(default="大功", max_length=20,null=True,blank=True, verbose_name="")  # 出勤類型
    attend_unit_11 = models.CharField(default="次", max_length=5,null=True,blank=True  , verbose_name="次數")  # 出勤單位
    attend_value_11 = models.DecimalField(max_digits=12,decimal_places=2,null=True,blank=True,verbose_name="次數")

    attend_type_12 = models.CharField(default="", max_length=20,null=True,blank=True, verbose_name="")  # 出勤類型
    attend_unit_12 = models.CharField(default="", max_length=5,null=True,blank=True  , verbose_name="")  # 出勤單位
    attend_value_12 = models.DecimalField( max_digits=12,decimal_places=2,null=True,blank=True,verbose_name="")


    def __str__(self):
        return "{} {}".format(self.work_code,self.attend_date)  # instance的值

    def __unicode__(self):
        return "{} {}".format(self.work_code,self.attend_date)  # instance的值

    class Meta:
        managed = True
        ordering = ('work_code','attend_date',)
        unique_together =  ('work_code','attend_date',)
        verbose_name = _("Employee Attendance Detail")
        verbose_name_plural = _("Employee Attendance Detail")


class EeAttendSummary(DictionaryMixin, AuditMixin, models.Model):
    work_code = models.ForeignKey(EmployeeInfoEasy, on_delete=models.CASCADE,related_name="ee_attend_summary",
                                  null=True, verbose_name="員工工號")  # 工號
    date_yyyy = models.PositiveSmallIntegerField(validators=[MinValueValidator(2020),MaxValueValidator(2100)],
                                                 verbose_name="年度")              # 西元年4位
    attend_type_01 = models.CharField(default="事假",max_length=20,null=True,blank=True,verbose_name="")           #出勤類型
    attend_unit_01 = models.CharField(default="天", max_length=5,null=True,blank=True ,verbose_name="天數")        #出勤單位
    attend_value_01 = models.DecimalField( max_digits=12,decimal_places=2,null=True,blank=True,verbose_name="天數")

    attend_type_02 = models.CharField(default="病假",max_length=20,null=True,blank=True,verbose_name="")           #出勤類型
    attend_unit_02 = models.CharField(default="天", max_length=5,null=True,blank=True ,verbose_name="天數")        #出勤單位
    attend_value_02 = models.DecimalField( max_digits=12,decimal_places=2,null=True,blank=True,verbose_name="天數")

    attend_type_03 = models.CharField(default="曠工", max_length=20,null=True,blank=True, verbose_name="")  # 出勤類型
    attend_unit_03 = models.CharField(default="天", max_length=5,null=True,blank=True  , verbose_name="天數")  # 出勤單位
    attend_value_03 = models.DecimalField( max_digits=12,decimal_places=2,null=True,blank=True,verbose_name="天數")  # 遲到 / 次

    attend_type_04 = models.CharField(default="遲到", max_length=20,null=True,blank=True, verbose_name="")  # 出勤類型
    attend_unit_04 = models.CharField(default="次", max_length=5,null=True,blank=True  , verbose_name="次數")  # 出勤單位
    attend_value_04 = models.DecimalField( max_digits=12,decimal_places=2,null=True,blank=True,verbose_name="次數")  # 遲到 / 次

    attend_type_05 = models.CharField(default="早退", max_length=20,null=True,blank=True,verbose_name="")           #出勤類型
    attend_unit_05 = models.CharField(default="次", max_length=5,null=True,blank=True ,verbose_name="次數")    #出勤單位
    attend_value_05 = models.DecimalField( max_digits=12,decimal_places=2,null=True,blank=True,verbose_name="次數")

    attend_type_06 = models.CharField(default="申誡", max_length=20,null=True,blank=True,verbose_name="")           #出勤類型
    attend_unit_06 = models.CharField(default="次", max_length=5,null=True,blank=True ,verbose_name="次數")    #出勤單位
    attend_value_06 = models.DecimalField( max_digits=12,decimal_places=2,null=True,blank=True,verbose_name="次數")

    attend_type_07 = models.CharField(default="小過", max_length=20,null=True,blank=True, verbose_name="")  # 出勤類型
    attend_unit_07 = models.CharField(default="次", max_length=5,null=True,blank=True  , verbose_name="次數")  # 出勤單位
    attend_value_07 = models.DecimalField( max_digits=12,decimal_places=2,null=True,blank=True,verbose_name="次數")

    attend_type_08 = models.CharField(default="大過", max_length=20,null=True,blank=True, verbose_name="")  # 出勤類型
    attend_unit_08 = models.CharField(default="次", max_length=5,null=True,blank=True  , verbose_name="次數")  # 出勤單位
    attend_value_08 = models.DecimalField( max_digits=12,decimal_places=2,null=True,blank=True,verbose_name="次數")

    attend_type_09 = models.CharField(default="嘉獎", max_length=20,null=True,blank=True, verbose_name="")  # 出勤類型
    attend_unit_09 = models.CharField(default="次", max_length=5,null=True,blank=True  , verbose_name="次數")  # 出勤單位
    attend_value_09 = models.DecimalField( max_digits=12,decimal_places=2,null=True,blank=True,verbose_name="次數")

    attend_type_10 = models.CharField(default="小功", max_length=20,null=True,blank=True, verbose_name="")  # 出勤類型
    attend_unit_10 = models.CharField(default="次", max_length=5,null=True,blank=True  , verbose_name="次數")  # 出勤單位
    attend_value_10 = models.DecimalField( max_digits=12,decimal_places=2,null=True,blank=True,verbose_name="次數")

    attend_type_11 = models.CharField(default="大功", max_length=20,null=True,blank=True, verbose_name="")  # 出勤類型
    attend_unit_11 = models.CharField(default="次", max_length=5,null=True,blank=True  , verbose_name="次數")  # 出勤單位
    attend_value_11 = models.DecimalField( max_digits=12,decimal_places=2,null=True,blank=True,verbose_name="次數")

    attend_type_12 = models.CharField(default="", max_length=20,null=True,blank=True, verbose_name="")  # 出勤類型
    attend_unit_12 = models.CharField(default="", max_length=5,null=True,blank=True  , verbose_name="")  # 出勤單位
    attend_value_12 = models.DecimalField( max_digits=12,decimal_places=2,null=True,blank=True,verbose_name="")



    def __str__(self):
        return "{} {}".format(self.work_code,self.date_yyyy)   # instance的值

    def __unicode__(self):
        return "{} {}".format(self.work_code,self.date_yyyy)   # instance的值

    class Meta:
        managed = True
        ordering = ('work_code','date_yyyy',)
        unique_together = ('work_code','date_yyyy',)
        verbose_name = _("Employee Attendance Summary")
        verbose_name_plural = _("Employee Attendance Summarys")
'''