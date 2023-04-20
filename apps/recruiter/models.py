# from django.db import models
# from django.urls import reverse
# from datetime import datetime, timedelta
# from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
# from django.utils.translation import gettext_lazy as _
# from django.utils.timezone import now
#
# from common.mixins import DictionaryMixin, AuditMixin
# from common.models import UserDefCode
#
# import sys
#
#
# def upload_article_cover(instance, filename):
#     ext = filename.split('.')[-1]  # 取出原本的副檔名
#     filename = '{}.{}'.format(instance, ext)  # return self.chi_name
#     year = datetime.now().year
#     return "images/apps/recruiter/employee/{0}/{1}".format(year, filename)
#
#
#
# # def udc_choice(field_name):
#     # __package__.rsplit('.', 1)    result-->['apps', 'recruiter']
#     # app_name = __package__.rsplit('.', 1)[-1]  # 取得app的名稱
#     # return {'topic_code': field_name}
#
#
# class EmployeeInfo(DictionaryMixin, AuditMixin, models.Model):
#     # blank=True, null=True 報到之前, 人資輸入資料(姓名/所屬公司/所屬部門...)
#     model_name = 'EmployeeInfo'
#     # card_regex = RegexValidator(regex=r'^([0-9]{8}$',message=_("Input your concact phone-number"))
#     # eng_regex = RegexValidator(regex=r'^([A-Z]{1}[a-z]{1}[a-zA-Z]{1,18}$',message=_("Input your concact phone-number"))
#     # phone_regex = RegexValidator(regex=r'^(0[0-9]{2,3})[0-9]{6,7}$',message=_("Input your concact phone-number"))
#     # mobile_regex = RegexValidator(regex=r'^09[0-9]{2}-[0-9]{6}$',message=_("Input your mobile phone-number"))
#     # id_card_regex = RegexValidator(regex=r'^[A-Z]{1}[0-9]{9}$',message=_("Input your id-card number"))
#     # work_code=models.CharField(validators=[card_regex], max_length=8, blank=True, null=True,verbose_name=_("Work Number"))  # 工號
#     work_code = models.CharField(unique=True, max_length=8, blank=True, null=True, verbose_name=_("Work Number"))  # 工號
#     card_code = models.CharField(unique=True, max_length=8, blank=True, null=True,
#                                  verbose_name=_("Card Number"))  # 刷卡片號碼
#     chi_name = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Employee Chinese Name"))  # 中文姓名
#     eng_name = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Employee English Name"))  # 英文姓名
#     mug_shot = models.ImageField(upload_to=upload_article_cover, blank=True, null=True,
#                                  verbose_name=_("Mug shot - Image File"))  # 大頭照(證件照) 存檔名稱:中文名字　　　
#     corp_id = models.ForeignKey(UserDefCode, on_delete='CASCADE', limit_choices_to={'topic_code':'corp_id'},
#                                 related_name="corp_id",blank=True, null=True,
#                                 verbose_name=_("Company Code"))  # (User defined code-最長8碼)所屬公司
#     dept_id = models.ForeignKey(UserDefCode, on_delete='CASCADE', limit_choices_to={'topic_code':'dept_id'},
#                                 related_name="dept_id",blank=True, null=True,
#                                 verbose_name=_("Department Code"))  # (User defined code-最長8碼)所屬部門
#     pos_id = models.ForeignKey(UserDefCode, on_delete='CASCADE', limit_choices_to={'topic_code':'pos_id'},
#                                related_name="pos_id",blank=True, null=True,
#                                verbose_name=_("Position Code"))  # (User defined code-最長8碼)主要職位
#     director_id = models.ForeignKey('self', on_delete=models.CASCADE,related_name="director_id_0",blank=True, null=True,
#                                     verbose_name=_("Direct supervisor"))  # 直屬主管(先手key姓名, 到時後, 再依"工號"..存工號)
#     factory_id = models.ForeignKey(UserDefCode, on_delete='CASCADE',related_name="factory_id",
#                                    limit_choices_to={'topic_code':'factory_id'},
#                                    blank=True, null=True, verbose_name=_("Factory area"))  # 辦公室(座位)的廠區
#     dl_idl = models.ForeignKey(UserDefCode, on_delete='CASCADE', limit_choices_to={'topic_code':'dl_idl'},
#                                related_name="dl_idl",blank=True, null=True,
#                                verbose_name=_("Direct Labor / Indirect Labor"))  # (User defined code-最長8碼)直/間接/
#     arrival_date = models.DateField(default=datetime.today(), blank=True, null=True,
#                                     verbose_name=_("Arrive at position date"))  # 到職日期, 預設等於當日
#     insurance_date = models.DateField(default=datetime.today(), blank=True, null=True,
#                                       verbose_name=_("Insured start date"))  # 投保日期, 預設等於當日
#     birth_date = models.DateField(blank=True, null=True, verbose_name=_("Employee's Birthday"))  # 生日
#     id_card_num = models.CharField(unique=True, blank=True, null=True, max_length=10,
#                                    verbose_name=_("Id Card Number"))  # 身份証號碼(台灣10碼),外國人,另選其他欄位
#     gender_id = models.ForeignKey(UserDefCode, on_delete='CASCADE',related_name="gender_id",
#                                   limit_choices_to={'topic_code':'gender_id'},
#                                   blank=True, null=True, verbose_name=_("Gender"))  # (User defined code-最長8碼)性別
#     height = models.IntegerField(blank=True, null=True, verbose_name=_("Employee's body height"))  # 身高
#     weight = models.IntegerField(blank=True, null=True, verbose_name=_("Employee's body weight"))  # 體重
#     blood_type = models.ForeignKey(UserDefCode, on_delete='CASCADE',related_name="blood_type",
#                                    limit_choices_to={'topic_code':'blood_type'},
#                                    blank=True, null=True, verbose_name=_("Blood Type"))  # (User defined code-最長8碼)性別
#     marrige_id = models.ForeignKey(UserDefCode, on_delete='CASCADE',related_name="marrige_id",
#                                    limit_choices_to={'topic_code':'marrige_id'},
#                                    blank=True, null=True,
#                                    verbose_name=_("Marriged Status"))  # (User defined code-最長8碼)婚姻狀態
#     educ_id = models.ForeignKey(UserDefCode, on_delete='CASCADE', limit_choices_to={'topic_code':'educ_id'},
#                                 related_name="educ_id",blank=True, null=True,
#                                 verbose_name=_("Highest Education"))  # (User defined code-最長8碼)最高學歷
#     major = models.TextField(blank=True, null=True, verbose_name=_("Major subjet"))  # 主修專業
#     ht_province = models.ForeignKey(UserDefCode, on_delete='CASCADE',
#                                     limit_choices_to={'topic_code':'ht_province'},
#                                     related_name="ht_province",blank=True, null=True,
#                                     verbose_name=_("Hometown(Province)"))  # (User defined code-最長8碼)籍貫-省
#     ht_city = models.ForeignKey(UserDefCode, on_delete='CASCADE', limit_choices_to={'topic_code':'ht_city'},
#                                 related_name="ht_city",blank=True, null=True,
#                                 verbose_name=_("Hometown(City)"))  # (User defined code-最長8碼)籍貫-市
#     reg_postcode = models.CharField(max_length=6, blank=True, null=True,
#                                     verbose_name=_("Registered post code"))  # 戶籍郵遞區號
#     reg_address = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Registered Address"))  # 戶籍地址
#     reg_phone = models.CharField(max_length=10, blank=True, null=False, verbose_name=_("Register phone number"))  # 戶籍電話
#     mail_postcode = models.CharField(max_length=6, blank=True, null=True, verbose_name=_("Mailing post code"))  # 通訊郵遞區號
#     mail_address = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Mailing address"))  # 通訊地址
#     mail_phone = models.CharField(max_length=10, blank=True, null=True, verbose_name=_("Contact phone number"))  # 通訊電話
#     mobile_phone = models.CharField(unique=True, max_length=10, blank=True, null=True,
#                                     verbose_name=_('Mobile phone number'))  # 手機號碼
#     expat_will = models.ForeignKey(UserDefCode, on_delete='CASCADE',
#                                    limit_choices_to={'topic_code':'expat_will'},
#                                    related_name="expact_will",blank=True, null=True,
#                                    verbose_name=_("Expatriate will"))  # (User defined code-最長8碼)國外長駐意向
#     expat_country = models.ForeignKey(UserDefCode, on_delete='CASCADE',
#                                       limit_choices_to={'topic_code':'expat_country'},
#                                       related_name="expact_country",blank=True, null=True,
#                                       verbose_name=_("Expatriate country"))  # (User defined code-最長8碼)長駐區域
#     depend_nums = models.IntegerField(blank=True, null=True, verbose_name=_("Number of Dependents"))  # 扶養人數
#     intr_chi_name = models.CharField(blank=True, null=True, max_length=20,
#                                      verbose_name=_("Introducer's Chinese Name"))  # 介紹人姓名
#     intr_dept_id = models.ForeignKey(UserDefCode, blank=True, null=True, on_delete='CASCADE',
#                                      related_name="intr_dept_id",limit_choices_to={'topic_code':'dept_id'},
#                                      verbose_name=_("Introducer's Department Code"))  # (User defined code-最長8碼)介紹人所屬部門
#     intr_pos_id = models.ForeignKey(UserDefCode, blank=True, null=True, on_delete='CASCADE',
#                                     related_name="intr_pos_id",limit_choices_to={'topic_code':'pos_id'},
#                                     verbose_name=_("Introducer's Position Code"))  # (User defined code-最長8碼)介紹人職位
#     intr_ship = models.CharField(blank=True, null=True, max_length=10,
#                                  verbose_name=_("Relationship with Introducer"))  # 與介紹人關係
#     transport1 = models.ForeignKey(UserDefCode, on_delete='CASCADE',
#                                    limit_choices_to={'topic_code':'transport'},
#                                    related_name="transport1",blank=True, null=True,
#                                    verbose_name=_("Transportation1"))  # (User defined code-最長8碼)交通工具1
#     trans1_licnum = models.CharField(max_length=10, blank=True, null=True,
#                                      verbose_name=_("Transportation1 - License plate number"))  # 交通工具1-車牌號碼
#     trans1_exhaust = models.IntegerField(blank=True, null=True, verbose_name=_("Transportation1 exhaust"))  # 交通工具1-排汽量
#     transport2 = models.ForeignKey(UserDefCode, blank=True, null=True, on_delete='CASCADE',
#                                    related_name="transport2",limit_choices_to={'topic_code':'transport'},
#                                    verbose_name=_("Transportation2"))  # (User defined code-最長8碼)交通工具2
#     trans2_licnum = models.CharField(max_length=10, blank=True, null=True,
#                                      verbose_name=_("Transportation2 - License plate number"))  # 交通工具2-車牌號碼
#     trans2_exhaust = models.IntegerField(blank=True, null=True, verbose_name=_("Transportation2 exhaust"))  # 交通工具1-排汽量
#     meals_partner = models.BooleanField(blank=True, null=True, verbose_name=_("Meals join as partner"))  # 搭伙註記 是/否
#     labor_pension_yn = models.BooleanField(blank=True, null=True,verbose_name=_("Labor pension yes/no"))  # 勞退自提 是/否
#     labor_pension_p = models.PositiveSmallIntegerField(blank=True, null=True,validators=[MinValueValidator(1), MaxValueValidator(6)],
#                                                        verbose_name=_("Labor Pension percent"))  # 勞退自提 比率   0~32767
#     labor_pension_sd = models.DateField(default=now(), blank=True, null=True, verbose_name=_("Labor pension start date"))  # 勞退自提 開始日,預設等於當日
#     lp_ed = now() + timedelta(days=36500)
#     labor_pension_ed = models.DateField(default=lp_ed, blank=True, null=True, verbose_name=_("Labor Pension end date"))  # 勞退自提 結束日,預設等於None
#     legal_case = models.CharField(max_length=20, blank=True, null=True,verbose_name=_("Legal case record"))  # 法律案件紀錄(memo)
#     memo_line = models.TextField(blank=True, null=True, verbose_name=_("Memo lines"))  # 註記(memo)
#     exporter = models.CharField(blank=True, null=True, max_length=10,
#                                 verbose_name=_("Name of export to excel"))  # 資料匯出excel的人
#     export_time = models.DateTimeField(blank=True, null=True, auto_now_add=True, auto_created=True,
#                                        verbose_name=_("Time of export to excel"))  # 資料匯出excel的時間
#     siblings = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name=_("Sibling numbers"))  # 兄弟姐妹人數
#     sons = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name=_("Son numbers"))  # 兒子人數
#     daughters = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name=_("Daughter numbers"))  # 女兒人數
#
#     def __str__(self):
#         return self.chi_name  # instance的值
#
#     def __unicode__(self):
#         return self.chi_name  # instance的值
#
#     def get_absolute_url(self):
#         return reverse('image_detail', None, {'object_id': self.id})
#
#     def class_name(self):
#         return self.__class__.__name__
#         # With this way, whenever you called  EmployeeInfo.class_name() in python code(also in the template  {{EmployeeInfo.class_name}}) it will return
#         # class name which is 'EmployeeInfo'.
#
#     class Meta:
#         managed = True
#         # app_label = 'recruiter'
#         # db_table = 'EmployeeInfo'
#         ordering = ('work_code',)
#         unique_together = ('work_code',)
#         verbose_name = _('Employee Information')
#         verbose_name_plural = _('Employees Informations')
#
#         # In other class or view , you cna get the model name
#         # EmployeeInfo._meta.verbose_name
#
#
# class EducBackground(DictionaryMixin, AuditMixin, models.Model):
#     educ_sys_choices = [
#         ('A','國中'),
#         ('B','高中'),
#         ('C','二專'),
#         ('D','三專'),
#         ('E','五專'),
#         ('F','大學'),
#         ('G','碩士'),
#         ('H','博士'),
#     ]
#
#     grad_status_choices = [
#         ('XX','在學'),
#         ('YY','畢業'),
#         ('ZZ','肄業'),
#     ]
#     employee = models.ForeignKey(EmployeeInfo,on_delete=models.CASCADE,related_name="educ_back",
#                                     verbose_name=_("EmployeeInfo model's primary key"))  # 新進員工『流水號』
#     school_name = models.CharField(max_length=20, verbose_name=_("Full school name"))  # 學校名稱
#     educ_sys = models.CharField(max_length=10,choices=educ_sys_choices,verbose_name=_("Education system"))  # 學制(國中/高中/二專/三專/五專/大學/碩士/博士
#     major_degree = models.CharField(max_length=10, verbose_name=_("Major/Degree"))  # 科/系
#     major_years = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)],verbose_name=_("Major Years"))  # 修業年限
#     major_sd = models.DateField(verbose_name=_("Enrollment date"))  # 生效日期
#     major_ed = models.DateField(blank=True, null=True, verbose_name=_("Graduated date"))  # 失效日期
#     grad_status = models.CharField(max_length=10,choices=grad_status_choices,verbose_name=_("Graduated status"))  # 狀態(畢業/肄業/在職)
#
#     def __str__(self):
#         return self.school_name+"."+self.educ_sys
#
#     def __unicode__(self):
#         return self.school_name+"."+self.educ_sys
#
#     class Meta:
#         managed = True
#         # app_label = 'recruiter'
#         # db_table = 'EducBack'
#         unique_together = (('employee','school_name','educ_sys','major_degree'))         #新人流水號+學校名稱+學制+主修名稱不可重覆
#         verbose_name = _('Education Background')
#         verbose_name_plural = _('Education Backgrounds')
#
#
# class CertificateLicense(DictionaryMixin, AuditMixin, models.Model):
#     # 証照檔
#     employee = models.ForeignKey(EmployeeInfo, on_delete=models.CASCADE,related_name="cert_lic",
#                                     verbose_name=_("EmployeeInfo model's primary key"))  # 新進員工『流水號』
#     license_code = models.CharField(unique=True,max_length=15, verbose_name=_("Certificate or License code"))  # 証照號碼唯一值
#     license_name = models.CharField(max_length=30, verbose_name=_("Certificate or License name"))  # 証照名稱
#     license_sd = models.DateField(verbose_name=_("Certificate/License effective date"))  # 生效日期
#     license_ed = models.DateField(blank=True, null=True, verbose_name=_("Certificate/License expiration date"))  # 失效日期
#
#     def __str__(self):
#         return self.license_name
#
#     def __unicode__(self):
#         return self.license_name
#
#     class Meta:
#         managed = True
#         # app_label = 'recruiter'
#         # db_table = 'CertLic'
#         unique_together = (('employee','license_code'),('employee','license_name'))         #新人流水號+証照名稱<or 號碼>(同一個人的証照名稱<or 號碼>不可重覆)
#         verbose_name = _('Certificate / License')
#         verbose_name_plural = _('Certificates / Licenses')
#
#
# class ExpertiseSkill(DictionaryMixin, AuditMixin, models.Model):
#     # 專長／技能檔
#     employee = models.ForeignKey(EmployeeInfo, on_delete=models.CASCADE,related_name="expert_skill",
#                                  verbose_name=_("EmployeeInfo model's primary key"))  # 新進員工『流水號』
#     expert_type = models.CharField(max_length=10,verbose_name=_("Expert or skill type"))  # 專長/技術類型
#     expert_name = models.CharField(max_length=10,verbose_name=_("Expert or skill name"))  # 專長/技術名稱
#
#     def __str__(self):
#         return self.expert_name
#
#     def __unicode__(self):
#         return self.expert_name
#
#     class Meta:
#         managed = True
#         # app_label = 'recruiter'
#         # db_table = 'ExpertSkill'
#         unique_together = ('employee','expert_name')         #新人流水號+專長名稱(同一個人的專長名稱不可重覆)
#         verbose_name = _('Expertise / Skill')
#         verbose_name_plural = _('Expertises / Skills')
#
#
# class WorkExperience(DictionaryMixin, AuditMixin, models.Model):
#     # 工作經歷
#     employee = models.ForeignKey(EmployeeInfo, on_delete=models.CASCADE,related_name="work_exp",
#                                     verbose_name=_("EmployeeInfo model's primary key"))  # 新進員工『流水號』
#     comp_name = models.CharField(max_length=20, verbose_name=_("Company Name"))          # 公司名稱
#     pos_name = models.CharField(max_length=20, verbose_name=_("Job Title"))          # 職位名稱
#     rsn_lvg = models.CharField(blank=True, null=True, max_length=20, verbose_name=_("Reason for leaving"))  #離職原因
#     salary = models.PositiveIntegerField(blank=True, null=True,
#                                          verbose_name=_("Salary"))  # 正數的整數 0~2147483647 薪水
#     employed_sd = models.DateField(verbose_name=_("Date of employment"))  # 受僱日期
#     employed_ed = models.DateField(blank=True, null=True,
#                                    verbose_name=_("Date for leaving"))  # 離職日期
#
#     def __str__(self):
#         return self.comp_name+" "+self.pos_name
#
#     def __unicode__(self):
#         return self.comp_name+" "+self.pos_name
#
#     class Meta:
#         managed = True
#         # app_label = 'recruiter'
#         # db_table = 'WorkExp'
#         unique_together = ('employee','comp_name','pos_name')   # 新人流水號+公司名稱+職位(同一個人的同一公司,不可有重覆職位)
#         verbose_name = _('Work Experience')
#         verbose_name_plural = _('Work Experiences')
#
#
# class FamilyStauts(DictionaryMixin, AuditMixin, models.Model):
#     # 家庭狀況
#     ship_choices = [
#         ('Father', '父親'),
#         ('Mother', '母親'),
#         ('Spouse', '配偶'),
#         ('others', '其他'),
#     ]
#     employee = models.ForeignKey(EmployeeInfo, on_delete=models.CASCADE,related_name="family_status",
#                                     verbose_name=_("EmployeeInfo model's primary key"))  # 新進員工『流水號』
#     ship = models.CharField(max_length=10, choices=ship_choices, verbose_name=_("Relationship with introducer"))  # 關係
#     name = models.CharField(max_length=20, verbose_name=_("Relative's name "))  # 名字
#     status = models.BooleanField(verbose_name=_("Exist ? "))  # 存/殁
#
#     def __str__(self):
#         return self.ship+" "+self.name
#
#     def __unicode__(self):
#         return self.ship+" "+self.name
#
#     class Meta:
#         managed = True
#         # app_label = 'recruiter'
#         # db_table = 'FamilyStats'
#         unique_together = ('employee', 'name')  # 新人流水號+名稱(跟一個人不可有重覆的關係)
#         verbose_name = _('Family Stauts')
#         verbose_name_plural = _("Family Member's Stauts")
#
#
# class Dependent_NHI(DictionaryMixin, AuditMixin, models.Model):
#     # 眷保
#     ship_choices = [
#         ('Father', '父親'),
#         ('Mother', '母親'),
#         ('Spouse', '配偶'),
#         ('Son', '兒子'),
#         ('Daughters', '女兒'),
#     ]
#     employee = models.ForeignKey(EmployeeInfo, on_delete=models.CASCADE,related_name="depend_NHI",
#                                     verbose_name=_("EmployeeInfo model's primary key"))  # 新進員工『流水號』
#     ship = models.CharField(max_length=10, choices=ship_choices, verbose_name=_("Relationship"))  # 關係
#     name = models.CharField(max_length=20, verbose_name=_("Related person's name "))  # 名字
#     birth_date = models.DateField(blank=True, null=True, verbose_name=_("Related person's Birthday"))  # 生日
#     id_card_num = models.CharField(unique=True, blank=True, null=True, max_length=10,
#                                    verbose_name=_("Relative's id-card Number"))  # 身份証號碼(台灣10碼),外國人,另選其他欄位
#
#     def __str__(self):
#         return self.ship+" "+self.name
#
#     def __unicode__(self):
#         return self.ship+" "+self.name
#
#     class Meta:
#         managed = True
#         # app_label = 'recruiter'
#         # db_table = 'DependNHI'
#         unique_together = ('employee', 'name')  # 新人流水號+名稱(跟一個人不可填兩次)
#         verbose_name = _('Dependent NHI')
#         verbose_name_plural = _("National Halth Insurance for family members")
#
#
# class EmergencyContact(DictionaryMixin, AuditMixin, models.Model):
#     # 緊急連絡人
#     ship_choices = [
#         ('Father', '父親'),
#         ('Mother', '母親'),
#         ('Spouse', '配偶'),
#         ('sibling', '兄弟姐妹'),
#         ('som', '兒子'),
#         ('daughter', '女兒'),
#         ('friend', '朋友'),
#         ('others', '其他'),
#     ]
#     employee = models.ForeignKey(EmployeeInfo, on_delete=models.CASCADE,related_name="emerg_contact",
#                                     verbose_name=_("EmployeeInfo model's primary key"))  # 新進員工『流水號』
#     ship = models.CharField(max_length=10, choices=ship_choices, verbose_name=_("Relationship with emergency contacts"))  # 關係
#     name = models.CharField(max_length=20, verbose_name=_("Relative's name "))  # 名字
#     mail_address = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Registered Address"))  # 通訊地址
#     mail_phone = models.CharField(max_length=10, blank=True, null=False, verbose_name=_("Registered phone number"))  # 通訊電話
#     sector = models.CharField(max_length=20,blank=True, null=True, verbose_name=_("Sector"))  # 服務單位
#     position = models.CharField(max_length=20,blank=True, null=True, verbose_name=_("Job Title"))  # 職位
#
#     def __str__(self):
#         return self.ship+" "+self.name
#
#     def __unicode__(self):
#         return self.ship+" "+self.name
#
#     class Meta:
#         managed = True
#         # app_label = 'recruiter'
#         # db_table = 'EmergContact'
#         unique_together = ('employee', 'name')  # 新人流水號+名稱(一個人的名稱不可填兩次)
#         verbose_name = _('Emergency contact')
#         verbose_name_plural = _("Emergency contacts")
