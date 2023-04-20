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
from apps.kpi.models import EmployeeInfoEasy

from django.utils import timezone

current_tz = timezone.get_current_timezone()
now = timezone.now().astimezone(current_tz).strftime('%Y-%m-%d')

choice_language = settings.LANGUAGES

# 工作職務檔
class JobTitle(DictionaryMixin, AuditMixin, models.Model):
    job_code = models.CharField(primary_key=True, max_length=8, blank=True, verbose_name="職務代號")
    job_name = models.CharField(max_length=32, blank=True, verbose_name="職務名稱")
    job_desc = models.CharField(max_length=200, blank=True, verbose_name="職務說明")
    level_number = models.PositiveSmallIntegerField(default=0,verbose_name="階層")
    job_parent = models.ForeignKey('self',on_delete=models.SET_NULL,to_field=('job_code'),
                                    related_name="job_parent_1",blank=True, null=True,
                                    verbose_name="上一階")

    def __str__(self):
        return '%s %s' % (self.job_code,self.job_name)  # instance的值

    def __unicode__(self):
        return '%s %s' % (self.job_code,self.job_name)

    class Meta:
        managed = True
        ordering = ('job_code',)
        verbose_name = "工作職務檔"
        verbose_name_plural = "工作職務檔"



# 職能的定義 Competence Competency Competencies Competent
# 工作職能檔 : 因為Competence太長了，寫程式過程有礙程式碼的維護，因此用skill取代Competence
class JobSkill(DictionaryMixin, AuditMixin, models.Model):
    skill_class = models.ForeignKey(UserDefCode, on_delete='CASCADE', limit_choices_to={'topic_code':'skill_class_id'},
                                related_name="skill_class_id",blank=True, null=True,
                                verbose_name="職能分類")   # 管理職需盤點 / 處階含以上主管需盤點 : UserDefineCode 的 shc1/shc2 做判斷
    # skill_level : 來源為職務的第二階編號(4位)，只有在 skill_class = '專業職能'時，此欄才會enable
    job_level = models.ForeignKey(JobTitle, on_delete='CASCADE', limit_choices_to={'level_number':2},
                                related_name="job_skill",blank=True, null=True,
                                verbose_name="專業職能類別")
    # 編碼由系統『根據 skill_class(二碼)+skill_level(4碼)+"-"+流水號(3碼)』自動產生
    skill_code = models.CharField(primary_key=True, max_length=10, blank=True, verbose_name="職能代號")
    skill_name = models.CharField(max_length=150, blank=True, verbose_name="職能名稱")
    skill_desc = models.CharField(max_length=300, blank=True, verbose_name="職能敍述")
    # 盤點與否(依EmployeeInfoEasy.pos<職位>在UserDefCode.shc1來比對盤點與否)
    chk_yn = models.CharField(default='Y',max_length=1, blank=True, verbose_name="盤點與否")

    def __str__(self):
        return '%s %s' % (self.skill_code,self.skill_name)  # instance的值

    def __unicode__(self):
        return '%s %s' % (self.skill_code,self.skill_name)

    class Meta:
        managed = True
        ordering = ('skill_code',)
        verbose_name = "工作職能檔"
        verbose_name_plural = "工作職能檔"


# 職務綁定職能檔
class JobTitleSkill(DictionaryMixin, AuditMixin, models.Model):
    job_title = models.ForeignKey('JobTitle',related_name='job_title_skill',on_delete='CASCADE', limit_choices_to={'level_number':3},null=True,verbose_name="職務代號")
    # order_number : 自動編碼，不可修改，由系統自動產生
    order_number = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),MaxValueValidator(999)],verbose_name="順序")
    job_skill = models.ForeignKey('JobSkill',related_name='job_title_skill',on_delete='CASCADE',null=True,verbose_name="職能代號")
    # 　enable : 新增時，預設為true
    enable = models.BooleanField(default=True,verbose_name=_("enable"))
    disable_date = models.DateField(blank=True, null=True,verbose_name="失效日期")
    enable_date = models.DateField(default=now,verbose_name="啟用日期")


    def __str__(self):
        return '%s %s' % (self.job_title,self.job_skill)  # instance的值

    def __unicode__(self):
        return '%s %s' % (self.job_title,self.skill_skill)

    class Meta:
        managed = True
        ordering = ('job_title','order_number')
        unique_together = ( ('job_title','job_skill',),('job_title','order_number',) )
        verbose_name = "職務綁定職能檔"
        verbose_name_plural = "職務綁定職能檔"


# 教育訓練方式
class StudyPlan(DictionaryMixin, AuditMixin, models.Model):
    study_code = models.PositiveSmallIntegerField(primary_key=True,validators=[MinValueValidator(1), MaxValueValidator(99)],verbose_name="學習代號")
    study_name = models.CharField(max_length=32, verbose_name="學習名稱")
    # 是 : 程式會出現『課程名稱』供使用者輸入    否:程式不會出現『課程名稱』
    study_course = models.CharField(default='',max_length=1,blank=True,null=True,verbose_name="輸入課程檢查")


    def __str__(self):
        return '%s %s' % (self.study_code,self.study_name)  # instance的值

    def __unicode__(self):
        return '%s %s' % (self.study_code,self.study_name)

    class Meta:
        managed = True
        ordering = ('study_code',)
        verbose_name = "教育訓練檔"
        verbose_name_plural = "教育訓練檔"


# 人員職務表
class EmployeeTitle(DictionaryMixin, AuditMixin, models.Model):
    work_code = models.ForeignKey(EmployeeInfoEasy,related_name='employee_title',on_delete='CASCADE',null=True,verbose_name="工號")     #工號
    job_title = models.ForeignKey('JobTitle',related_name='employee_title',on_delete='CASCADE',null=True,verbose_name="職務代號")
    dept_flevel = models.CharField(max_length=50, blank=True, null=True, verbose_name="一級部門")
    # 　enable : 上線匯入／新增時，預設為空白
    enable = models.BooleanField(default=True,verbose_name=_("enable"))
    disable_date = models.DateField(blank=True, null=True,verbose_name="失效日期")
    enable_date = models.DateField(default=now,verbose_name="啟用日期")

    def __str__(self):
        return '%s %s' % (self.work_code,self.job_title)  # instance的值

    def __unicode__(self):
        return '%s %s' % (self.work_code,self.job_title)

    class Meta:
        managed = True
        ordering = ('work_code','job_title',)
        unique_together = ('work_code','job_title',)
        verbose_name = "人員職務表"
        verbose_name_plural = "人員職務表"

def reports_path():
    return os.path.join(settings.MEDIA_ROOT,'/media-files/reports/pdf/')



# 技能矩陣:主檔
class MatrixStatus(DictionaryMixin, AuditMixin, models.Model):
    #TAB1(4位)+YEAR(4位)+MONTH(2位)+DAY(2位)+id(取3位) : 技能矩陣表
    #TAB2(4位)+YEAR(4位)+MONTH(2位)+DAY(2位)+id(取3位) : 工作事項明細表
    bpm_number = models.CharField(default='',primary_key=True,blank=True,max_length=15, verbose_name="BPM單號")
    bpm_yn = models.CharField(default='', blank=True, max_length=1, verbose_name="BPM已送")
    direct_supv =  models.ForeignKey(EmployeeInfoEasy, default=None,related_name="matrix_status", on_delete='CASCADE', null=True,  verbose_name="直接主管")
    dept_flevel = models.ForeignKey(UserDefCode, on_delete='CASCADE', limit_choices_to={'topic_code':'dept_flevel_id'},
                                related_name="matrix_status",blank=True, null=True,
                                verbose_name="一級部門")  # (User defined code-最長8碼)部門全稱 2021/07/02 add
    year = models.PositiveSmallIntegerField(validators=[MinValueValidator(2020), MaxValueValidator(2100)],verbose_name="年度")        # 西元年4位
    month = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)],verbose_name="月份")  # 月份2位
    report_name = models.FilePathField(default='',path=reports_path,verbose_name="報表名稱")
    report_url = models.URLField(default='',verbose_name="報表網址")

    bpm_status_desc1 = models.CharField(default='', max_length=30, blank=True, null=True, verbose_name="BPM狀態說明1")
    # bpm_status_desc2 = models.CharField(default='', max_length=30, blank=True, null=True, verbose_name="BPM狀態說明2")
    # bpm_status = models.ForeignKey(UserDefCode, on_delete='CASCADE', limit_choices_to={'topic_code':'bpm_status'},related_name="matrix_status", null=True,verbose_name="bpm狀態")
    subordinate = models.CharField(default="",max_length=320,verbose_name="下屬工號")

    def __str__(self):
        return '%s' % self.bpm_number  # instance的值

    def __unicode__(self):
        return '%s' % self.bpm_number

    class Meta:
        managed = True
        ordering = ('direct_supv','dept_flevel','year','month')
        unique_together = ('direct_supv','dept_flevel','year', 'month')
        verbose_name = "技能評核BPM"
        verbose_name_plural = "技能評核BPM"


# 技能矩陣:主檔
class MatrixMaster(DictionaryMixin, AuditMixin, models.Model):
    work_code_title = models.ForeignKey(EmployeeTitle, related_name="matrix_master", on_delete='CASCADE', null=True,
                                        verbose_name="員工職務")
    year = models.PositiveSmallIntegerField(validators=[MinValueValidator(2020), MaxValueValidator(2100)],verbose_name="年度")        # 西元年4位
    month = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)],verbose_name="月份")  # 月份2位
    bpm = models.ForeignKey(MatrixStatus,on_delete='CASCADE',default=None,related_name="matrix_master",blank=True,null=True,verbose_name="BPM單號")
    # last_status = models.ForeignKey(RegActRules, on_delete='CASCADE',related_name="matrix_master",blank=True, null=True,verbose_name="最後狀態")

    def __str__(self):
        return '%s %s' % (self.work_code_title,str(self.year)+'年'+str(self.month)+'月')  # instance的值

    def __unicode__(self):
        return '%s %s' % (self.work_code_title,str(self.year)+'年'+str(self.month)+'月')

    class Meta:
        managed = True
        ordering = ('work_code_title','year','month')
        unique_together = ('work_code_title','year','month')
        verbose_name = "技能評核主檔"
        verbose_name_plural = "技能評核主檔"



# 方案一 : 所有職能放在一起-----------------------------------------------------------------------------------------------------------------------BEGIN
#         優點:省去重覆的索引欄位，一檔包含全部，程式撰寫容易，
#         缺點:要預留『職能』增加的欄位，欄位很多
# 技能矩陣表( 所有職能放在一起 )
class MatrixDetail(DictionaryMixin, AuditMixin, models.Model):
    master = models.ForeignKey(MatrixMaster,primary_key=True,related_name="matrix_detail", on_delete='CASCADE',verbose_name="評核期間")

    # 核心職能 : 最多20個
    cr001 = models.CharField(max_length=1, blank=True, null=True, verbose_name="核心職能成熟度01")
    cr002 = models.CharField(max_length=1, blank=True, null=True, verbose_name="核心職能成熟度02")
    cr003 = models.CharField(max_length=1, blank=True, null=True, verbose_name="核心職能成熟度03")
    cr004 = models.CharField(max_length=1, blank=True, null=True, verbose_name="核心職能成熟度04")
    cr005 = models.CharField(max_length=1, blank=True, null=True, verbose_name="核心職能成熟度05")
    cr006 = models.CharField(max_length=1, blank=True, null=True, verbose_name="核心職能成熟度06")
    cr007 = models.CharField(max_length=1, blank=True, null=True, verbose_name="核心職能成熟度07")
    cr008 = models.CharField(max_length=1, blank=True, null=True, verbose_name="核心職能成熟度08")
    cr009 = models.CharField(max_length=1, blank=True, null=True, verbose_name="核心職能成熟度09")
    cr010 = models.CharField(max_length=1, blank=True, null=True, verbose_name="核心職能成熟度10")
    cr011 = models.CharField(max_length=1, blank=True, null=True, verbose_name="核心職能成熟度11")
    cr012 = models.CharField(max_length=1, blank=True, null=True, verbose_name="核心職能成熟度12")
    cr013 = models.CharField(max_length=1, blank=True, null=True, verbose_name="核心職能成熟度13")
    cr014 = models.CharField(max_length=1, blank=True, null=True, verbose_name="核心職能成熟度14")
    cr015 = models.CharField(max_length=1, blank=True, null=True, verbose_name="核心職能成熟度15")
    cr016 = models.CharField(max_length=1, blank=True, null=True, verbose_name="核心職能成熟度16")
    cr017 = models.CharField(max_length=1, blank=True, null=True, verbose_name="核心職能成熟度17")
    cr018 = models.CharField(max_length=1, blank=True, null=True, verbose_name="核心職能成熟度18")
    cr019 = models.CharField(max_length=1, blank=True, null=True, verbose_name="核心職能成熟度19")
    cr020 = models.CharField(max_length=1, blank=True, null=True, verbose_name="核心職能成熟度20")

    # 一般職能 : 最多20個
    ge001 = models.CharField(max_length=1, blank=True, null=True, verbose_name="一般職能成熟度01")
    ge002 = models.CharField(max_length=1, blank=True, null=True, verbose_name="一般職能成熟度02")
    ge003 = models.CharField(max_length=1, blank=True, null=True, verbose_name="一般職能成熟度03")
    ge004 = models.CharField(max_length=1, blank=True, null=True, verbose_name="一般職能成熟度04")
    ge005 = models.CharField(max_length=1, blank=True, null=True, verbose_name="一般職能成熟度05")
    ge006 = models.CharField(max_length=1, blank=True, null=True, verbose_name="一般職能成熟度06")
    ge007 = models.CharField(max_length=1, blank=True, null=True, verbose_name="一般職能成熟度07")
    ge008 = models.CharField(max_length=1, blank=True, null=True, verbose_name="一般職能成熟度08")
    ge009 = models.CharField(max_length=1, blank=True, null=True, verbose_name="一般職能成熟度09")
    ge010 = models.CharField(max_length=1, blank=True, null=True, verbose_name="一般職能成熟度10")
    ge011 = models.CharField(max_length=1, blank=True, null=True, verbose_name="一般職能成熟度11")
    ge012 = models.CharField(max_length=1, blank=True, null=True, verbose_name="一般職能成熟度12")
    ge013 = models.CharField(max_length=1, blank=True, null=True, verbose_name="一般職能成熟度13")
    ge014 = models.CharField(max_length=1, blank=True, null=True, verbose_name="一般職能成熟度14")
    ge015 = models.CharField(max_length=1, blank=True, null=True, verbose_name="一般職能成熟度15")
    ge016 = models.CharField(max_length=1, blank=True, null=True, verbose_name="一般職能成熟度16")
    ge017 = models.CharField(max_length=1, blank=True, null=True, verbose_name="一般職能成熟度17")
    ge018 = models.CharField(max_length=1, blank=True, null=True, verbose_name="一般職能成熟度18")
    ge019 = models.CharField(max_length=1, blank=True, null=True, verbose_name="一般職能成熟度19")
    ge020 = models.CharField(max_length=1, blank=True, null=True, verbose_name="一般職能成熟度20")

    # 管理職能 : 最多60個
    ma001 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度01")
    ma002 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度02")
    ma003 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度03")
    ma004 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度04")
    ma005 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度05")
    ma006 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度06")
    ma007 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度07")
    ma008 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度08")
    ma009 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度09")
    ma010 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度10")
    ma011 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度11")
    ma012 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度12")
    ma013 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度13")
    ma014 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度14")
    ma015 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度15")
    ma016 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度16")
    ma017 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度17")
    ma018 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度18")
    ma019 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度19")
    ma020 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度20")
    ma021 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度21")
    ma022 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度22")
    ma023 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度23")
    ma024 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度24")
    ma025 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度25")
    ma026 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度26")
    ma027 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度27")
    ma028 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度28")
    ma029 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度29")
    ma030 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度30")
    ma031 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度31")
    ma032 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度32")
    ma033 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度33")
    ma034 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度34")
    ma035 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度35")
    ma036 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度36")
    ma037 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度37")
    ma038 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度38")
    ma039 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度39")
    ma040 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度40")
    ma041 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度41")
    ma042 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度42")
    ma043 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度43")
    ma044 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度44")
    ma045 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度45")
    ma046 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度46")
    ma047 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度47")
    ma048 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度48")
    ma049 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度49")
    ma050 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度50")
    ma051 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度51")
    ma052 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度52")
    ma053 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度53")
    ma054 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度54")
    ma055 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度55")
    ma056 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度56")
    ma057 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度57")
    ma058 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度58")
    ma059 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度59")
    ma060 = models.CharField(max_length=1, blank=True, null=True, verbose_name="管理職能成熟度60")

    # 專業職能 : 最多120個
    pr001 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度01")
    pr002 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度02")
    pr003 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度03")
    pr004 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度04")
    pr005 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度05")
    pr006 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度06")
    pr007 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度07")
    pr008 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度08")
    pr009 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度09")
    pr010 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度10")
    pr011 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度11")
    pr012 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度12")
    pr013 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度13")
    pr014 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度14")
    pr015 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度15")
    pr016 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度16")
    pr017 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度17")
    pr018 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度18")
    pr019 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度19")
    pr020 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度20")
    pr021 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度21")
    pr022 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度22")
    pr023 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度23")
    pr024 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度24")
    pr025 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度25")
    pr026 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度26")
    pr027 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度27")
    pr028 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度28")
    pr029 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度29")
    pr030 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度30")
    pr031 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度31")
    pr032 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度32")
    pr033 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度33")
    pr034 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度34")
    pr035 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度35")
    pr036 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度36")
    pr037 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度37")
    pr038 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度38")
    pr039 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度39")
    pr040 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度40")
    pr041 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度41")
    pr042 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度42")
    pr043 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度43")
    pr044 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度44")
    pr045 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度45")
    pr046 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度46")
    pr047 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度47")
    pr048 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度48")
    pr049 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度49")
    pr050 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度50")
    pr051 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度51")
    pr052 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度52")
    pr053 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度53")
    pr054 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度54")
    pr055 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度55")
    pr056 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度56")
    pr057 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度57")
    pr058 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度58")
    pr059 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度59")
    pr060 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度60")
    pr061 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度61")
    pr062 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度62")
    pr063 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度63")
    pr064 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度64")
    pr065 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度65")
    pr066 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度66")
    pr067 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度67")
    pr068 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度68")
    pr069 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度69")
    pr070 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度70")
    pr071 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度71")
    pr072 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度72")
    pr073 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度73")
    pr074 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度74")
    pr075 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度75")
    pr076 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度76")
    pr077 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度77")
    pr078 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度78")
    pr079 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度79")
    pr080 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度80")
    pr081 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度81")
    pr082 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度82")
    pr083 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度83")
    pr084 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度84")
    pr085 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度85")
    pr086 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度86")
    pr087 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度87")
    pr088 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度88")
    pr089 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度89")
    pr090 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度90")
    pr091 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度91")
    pr092 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度92")
    pr093 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度93")
    pr094 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度94")
    pr095 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度95")
    pr096 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度96")
    pr097 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度97")
    pr098 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度98")
    pr099 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度99")
    pr100 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度100")
    pr101 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度101")
    pr102 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度102")
    pr103 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度103")
    pr104 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度104")
    pr105 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度105")
    pr106 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度106")
    pr107 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度107")
    pr108 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度108")
    pr109 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度109")
    pr110 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度110")
    pr111 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度111")
    pr112 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度112")
    pr113 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度113")
    pr114 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度114")
    pr115 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度115")
    pr116 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度116")
    pr117 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度117")
    pr118 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度118")
    pr119 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度119")
    pr120 = models.CharField(max_length=1, blank=True, null=True, verbose_name="專業職能成熟度120")
    # 小計
    xa001 = models.DecimalField(default=None,max_digits=6, decimal_places=2, null=True, verbose_name="加權平均")
    xa002 = models.CharField(default='',max_length=10, blank=True, verbose_name="總成熟度")
    # 教育訓練計劃
    xb001 = models.CharField(max_length=250, blank=True, verbose_name="教育訓練")
    xb002 = models.CharField(max_length=250, blank=True, verbose_name="課程名稱")
    xb003 = models.CharField(max_length=250, blank=True, null=True, verbose_name="預定輪調")  # 預定輪調規劃
    #---------------------------------------------------------------------------------------------------------------------

    def __str__(self):
        return '%s' % (self.master)  # instance的值

    def __unicode__(self):
        return '%s' % (self.master)

    class Meta:
        managed = True
        ordering = ('master',)
        verbose_name = "技能矩陣陣明細表"
        verbose_name_plural = "技能矩陣陣明細表"
# 方案一 : 所有職能放在一起-----------------------------------------------------------------------------------------------------------------------ENDING



# pdca定義
class PdcaDefinition(DictionaryMixin, AuditMixin, models.Model):
    # order_number : 自動編碼，不可修改，由系統自動產生
    order_number = models.PositiveSmallIntegerField(unique=True,validators=[MinValueValidator(1),MaxValueValidator(999)],verbose_name="順序")
    pdca_choices = (
        ('P','P') ,
        ('D','D') ,
        ('C','C'),
        ('A','A'),
    )
    pdca_choice = models.CharField(default='',max_length=1, choices=pdca_choices,blank=True, null=True, verbose_name="PDCA選擇")
    pdca_desc = models.CharField(unique=True,max_length=10,verbose_name="項目")
    enable = models.BooleanField(default=True, verbose_name=_("enable"))


    def __str__(self):
        return '%s %s' % (self.pdca_desc,self.pdca_choice)  # instance的值

    def __unicode__(self):
        return '%s %s' % (self.pdca_desc,self.pdca_desc)

    class Meta:
        managed = True
        ordering = ('order_number',)
        verbose_name = "PDCA定義檔"
        verbose_name_plural = "PDCA定義檔"


# flow定義
class FlowDefinition(DictionaryMixin, AuditMixin, models.Model):
    # order_number : 自動編碼，不可修改，由系統自動產生
    order_number = models.PositiveSmallIntegerField(unique=True,validators=[MinValueValidator(1),MaxValueValidator(999)],verbose_name="順序")
    flow_desc = models.CharField(default='',max_length=60,blank=True, null=True, verbose_name="流程")
    enable = models.BooleanField(default=True, verbose_name=_("enable"))


    def __str__(self):
        return '%s %s' % (self.order_number,self.flow_desc)  # instance的值

    def __unicode__(self):
        return '%s %s' % (self.order_number,self.flow_desc)

    class Meta:
        managed = True
        ordering = ('order_number',)
        verbose_name = "流程定義檔"
        verbose_name_plural = "流程定義檔"


# cycle定義
class CycleDefinition(DictionaryMixin, AuditMixin, models.Model):
    # order_number : 自動編碼，不可修改，由系統自動產生
    order_number = models.PositiveSmallIntegerField(unique=True,validators=[MinValueValidator(1),MaxValueValidator(999)],verbose_name="順序")
    cycle_desc = models.CharField(unique=True,default='',max_length=12,blank=True, null=True, verbose_name="週期")
    basic = models.IntegerField(default=1, verbose_name="分子")
    months = models.IntegerField(default=1, verbose_name="月份換算")
    enable = models.BooleanField(default=True, verbose_name="enable")

    def __str__(self):
        return '%s' % (self.cycle_desc)  # instance的值

    def __unicode__(self):
        return '%s' % (self.cycle_desc)

    class Meta:
        managed = True
        ordering = ('order_number',)
        verbose_name = "週期定義檔"
        verbose_name_plural = "週期定義檔"


# 工作事項:主檔
class PdcaMaster(DictionaryMixin, AuditMixin, models.Model):
    #TAB1(4位)+YEAR(4位)+MONTH(2位)+DAY(2位)+id(取3位) : 技能矩陣表
    #TAB2(4位)+YEAR(4位)+MONTH(2位)+DAY(2位)+id(取3位) : 工作事項明細表
    work_code = models.ForeignKey(EmployeeInfoEasy,related_name='pdca_master',on_delete=models.CASCADE,null=True,verbose_name='工號')     #工號
    the_time = models.IntegerField(verbose_name='填寫次數')                                                                               #第幾次填寫
    job_title = models.ForeignKey('JobTitle',related_name='pdca_master',on_delete='CASCADE',null=True,verbose_name='職務代號')
    bpm_number = models.CharField(default='',blank=True,max_length=15, verbose_name='BPM單號')
    bpm_yn = models.CharField(default='',blank=True,max_length=1, verbose_name='BPM已送')
    report_name = models.FilePathField(default='',path=reports_path,verbose_name='報表名稱')
    report_url = models.URLField(default='',verbose_name='報表網址')
    bpm_status_desc1 = models.CharField(default='', max_length=30, blank=True, null=True, verbose_name='BPM狀態說明1')
    exp_count = models.PositiveSmallIntegerField(default=0,verbose_name='匯出次數')  # 月份2位
    exp_time = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='匯出時間')

    def __str__(self):
        return '%s %s %s' % ('work_code','the_time','job_title')  # instance的值

    def __unicode__(self):
        return '%s %s %s' % ('work_code','the_time','job_title')

    class Meta:
        managed = True
        ordering = ('work_code','the_time','job_title')
        unique_together = ('work_code','the_time','job_title')
        verbose_name = "工作事項BPM"
        verbose_name_plural = "工作事項BPM"


# 工作事項:明細表
class PdcaDetail(DictionaryMixin, AuditMixin, models.Model):
    master = models.ForeignKey(PdcaMaster,on_delete=models.CASCADE,null=True,verbose_name='填寫次數')
    order_number = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(999)],verbose_name='順序')
    work_item = models.CharField(max_length=100, null=True, blank=True, verbose_name='工作項目')
    lang_code_in = models.CharField(default='',null=True,blank=True,max_length=7, verbose_name='輸入的語系')
    lang_code_out = models.CharField(default='', null=True, blank=True, max_length=7, verbose_name='翻譯的語系')
    fwork_item = models.CharField(max_length=500, null=True, blank=True, verbose_name='工作項目_外國語言')

    # pdca : 最多20個,分鐘數
    pdca01 = models.IntegerField( null=True, verbose_name="PDCA01")
    pdca02 = models.IntegerField( null=True, verbose_name="PDCA02")
    pdca03 = models.IntegerField( null=True, verbose_name="PDCA03")
    pdca04 = models.IntegerField( null=True, verbose_name="PDCA04")
    pdca05 = models.IntegerField( null=True, verbose_name="PDCA05")
    pdca06 = models.IntegerField( null=True, verbose_name="PDCA06")
    pdca07 = models.IntegerField( null=True, verbose_name="PDCA07")
    pdca08 = models.IntegerField( null=True, verbose_name="PDCA08")
    pdca09 = models.IntegerField( null=True, verbose_name="PDCA09")
    pdca10 = models.IntegerField( null=True, verbose_name="PDCA10")
    pdca11 = models.IntegerField( null=True, verbose_name="PDCA11")
    pdca12 = models.IntegerField( null=True, verbose_name="PDCA12")
    pdca13 = models.IntegerField( null=True, verbose_name="PDCA13")
    pdca14 = models.IntegerField( null=True, verbose_name="PDCA14")
    pdca15 = models.IntegerField( null=True, verbose_name="PDCA15")
    pdca16 = models.IntegerField( null=True, verbose_name="PDCA16")
    pdca17 = models.IntegerField( null=True, verbose_name="PDCA17")
    pdca18 = models.IntegerField( null=True, verbose_name="PDCA18")
    pdca19 = models.IntegerField( null=True, verbose_name="PDCA19")
    pdca20 = models.IntegerField( null=True, verbose_name="PDCA20")
    # 流程 : 12個, 文字內容
    flow_length=100
    flow01 = models.CharField( max_length=flow_length, null=True, blank=True, verbose_name="流程01")
    flow02 = models.CharField( max_length=flow_length, null=True, blank=True, verbose_name="流程02")
    flow03 = models.CharField( max_length=flow_length, null=True, blank=True, verbose_name="流程03")
    flow04 = models.CharField( max_length=flow_length, null=True, blank=True, verbose_name="流程04")
    flow05 = models.CharField( max_length=flow_length, null=True, blank=True, verbose_name="流程05")
    flow06 = models.CharField( max_length=flow_length, null=True, blank=True, verbose_name="流程06")
    flow07 = models.CharField( max_length=flow_length, null=True, blank=True, verbose_name="流程07")
    flow08 = models.CharField( max_length=flow_length, null=True, blank=True, verbose_name="流程08")
    flow09 = models.CharField( max_length=flow_length, null=True, blank=True, verbose_name="流程09")
    flow10 = models.CharField( max_length=flow_length, null=True, blank=True, verbose_name="流程10")
    flow11 = models.CharField( max_length=flow_length, null=True, blank=True, verbose_name="流程11")
    flow12 = models.CharField( max_length=flow_length, null=True, blank=True, verbose_name="流程12")
    # 流程 : 12個, 文字內容_foreign
    flow_length = 300
    fflow01 = models.CharField( max_length=flow_length, null=True, blank=True, verbose_name="流程01")
    fflow02 = models.CharField( max_length=flow_length, null=True, blank=True, verbose_name="流程02")
    fflow03 = models.CharField( max_length=flow_length, null=True, blank=True, verbose_name="流程03")
    fflow04 = models.CharField( max_length=flow_length, null=True, blank=True, verbose_name="流程04")
    fflow05 = models.CharField( max_length=flow_length, null=True, blank=True, verbose_name="流程05")
    fflow06 = models.CharField( max_length=flow_length, null=True, blank=True, verbose_name="流程06")
    fflow07 = models.CharField( max_length=flow_length, null=True, blank=True, verbose_name="流程07")
    fflow08 = models.CharField( max_length=flow_length, null=True, blank=True, verbose_name="流程08")
    fflow09 = models.CharField( max_length=flow_length, null=True, blank=True, verbose_name="流程09")
    fflow10 = models.CharField( max_length=flow_length, null=True, blank=True, verbose_name="流程10")
    fflow11 = models.CharField( max_length=flow_length, null=True, blank=True, verbose_name="流程11")
    fflow12 = models.CharField( max_length=flow_length, null=True, blank=True, verbose_name="流程12")
    # cycle
    cycl01 = models.CharField( max_length=30, null=True, blank=True, verbose_name="週期")           #事關計算問題, 只能用一個欄位(存多種語言), 先試看看吧!
    fcycl01 = models.CharField( max_length=30, null=True, blank=True, verbose_name="週期")          #暫時不使用( 2022/07/29 )
    cycl02 = models.CharField( max_length=3, null=True, verbose_name="次數(週期頻率)")


    # 分鐘合計
    calc01 = models.IntegerField(null=True, verbose_name="作業時間合計(分鐘/次)")
    calc02 = models.DecimalField(default=None,max_digits=10, decimal_places=2, null=True, verbose_name="每月合計分鐘數")

    # pdca小計
    ptot01 = models.DecimalField(default=None,max_digits=10, decimal_places=2, null=True, verbose_name="Plan小計")
    dtot01 = models.DecimalField(default=None,max_digits=10, decimal_places=2, null=True, verbose_name="Do小計")
    ctot01 = models.DecimalField(default=None,max_digits=10, decimal_places=2, null=True, verbose_name="Check1小計")
    ctot02 = models.DecimalField(default=None,max_digits=10, decimal_places=2, null=True, verbose_name="Check2小計")
    ctot03 = models.DecimalField(default=None,max_digits=10, decimal_places=2, null=True, verbose_name="Check3小計")
    ctot04 = models.DecimalField(default=None,max_digits=10, decimal_places=2, null=True, verbose_name="Check4小計")
    ctot05 = models.DecimalField(default=None,max_digits=10, decimal_places=2, null=True, verbose_name="Check5小計")
    ctot06 = models.DecimalField(default=None,max_digits=10, decimal_places=2, null=True, verbose_name="Check6小計")
    atot01 = models.DecimalField(default=None,max_digits=10, decimal_places=2, null=True, verbose_name="Action小計")

    #確認碼
    okyn01 = models.CharField(default="",max_length=10, verbose_name="確認")        #按下確認後,會計算,計算後改為True(也會做欄位檢查, 是否為0),送出bpm前, 若此欄為False不予送出

    def __str__(self):
        return '%s' % (self.master)  # instance的值

    def __unicode__(self):
        return '%s' % (self.master)

    class Meta:
        managed = True
        ordering = ('master','order_number')
        unique_together = ('master','order_number')
        verbose_name = "工作事項明細表"
        verbose_name_plural = "工作事項明細表"


# 工作職務檔_FOREIGN
class JobTitleForeign(DictionaryMixin, AuditMixin, models.Model):
    job_code = models.ForeignKey(JobTitle,on_delete=models.CASCADE,verbose_name="職務代號")
    lang_code = models.CharField(max_length=7,choices=choice_language,verbose_name="語系")
    job_name = models.CharField(max_length=100, blank=True, verbose_name="職務名稱")

    def __str__(self):
        return '%s %s %s' % (self.lang_code,self.job_code,self.job_name)  # instance的值

    def __unicode__(self):
        return '%s %s %s' % (self.lang_code,self.job_code,self.job_name)

    class Meta:
        managed = True
        ordering = ('lang_code','job_code',)
        unique_together = ('lang_code', 'job_code')
        verbose_name = "工作職務檔_外國語言"
        verbose_name_plural = "工作職務檔_外國語言"


# PDCA定義_FOREIGN
class PdcaDefinitionForeign(DictionaryMixin, AuditMixin, models.Model):
    pdca = models.ForeignKey(PdcaDefinition,on_delete=models.CASCADE,verbose_name="PDCA")
    lang_code = models.CharField(max_length=7,choices=choice_language,verbose_name="語系")
    pdca_desc = models.CharField(unique=True,max_length=30,verbose_name="PDCA說明")


    def __str__(self):
        return '%s %s' % (self.lang_code,self.pdca_desc)  # instance的值

    def __unicode__(self):
        return '%s %s' % (self.lang_code,self.pdca_desc)

    class Meta:
        managed = True
        ordering = ('pdca','lang_code')
        unique_together =  ('pdca','lang_code')
        verbose_name = "PDCA定義檔_外國語言"
        verbose_name_plural = "PDCA定義檔_外國語言"


# FLOW定義_FOREIGN
class FlowDefinitionForeign(DictionaryMixin, AuditMixin, models.Model):
    flow = models.ForeignKey(FlowDefinition,on_delete=models.CASCADE,verbose_name="FLOW")
    lang_code = models.CharField(max_length=7,choices=choice_language,verbose_name="語系")
    flow_desc = models.CharField(unique=True,max_length=180,verbose_name="FLOW說明")


    def __str__(self):
        return '%s %s' % (self.lang_code,self.flow_desc)  # instance的值

    def __unicode__(self):
        return '%s %s' % (self.lang_code,self.flow_desc)

    class Meta:
        managed = True
        ordering = ('flow','lang_code')
        unique_together =  ('flow','lang_code')
        verbose_name = "流程定義檔_外國語言"
        verbose_name_plural = "流程定義檔_外國語言"


# CYCLE定義_FOREIGN
class CycleDefinitionForeign(DictionaryMixin, AuditMixin, models.Model):
    cycle = models.ForeignKey(CycleDefinition,on_delete=models.CASCADE,verbose_name="CYCLE")
    lang_code = models.CharField(max_length=7,choices=choice_language,verbose_name="語系")
    cycle_desc = models.CharField(unique=True,max_length=30,verbose_name="CYCLE說明")


    def __str__(self):
        return '%s %s' % (self.lang_code,self.cycle_desc)  # instance的值

    def __unicode__(self):
        return '%s %s' % (self.lang_code,self.cycle_desc)

    class Meta:
        managed = True
        ordering = ('cycle','lang_code')
        unique_together =  ('cycle','lang_code')
        verbose_name = "週期定義檔_外國語言"
        verbose_name_plural = "週期定義檔_外國語言"


