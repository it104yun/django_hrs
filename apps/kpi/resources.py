from import_export import resources
from .models import EmployeeInfoEasy
    # ,EeAttendSummary
from datetime import datetime
import xlwt

class EmployeeInfoEasyResource(resources.ModelResource):
    class Meta:
        model = EmployeeInfoEasy
        # import_id_fields = ('corp',
        #                     'dept',
        #                     'director',
        #                     'factory',
        #                     'pos',
        #                     'bonus_factor',
        #                     'eval_class',
        #                     'nat',
        #                     'rank',)

    def before_save_instance(self, instance, using_transactions, dry_run):
        # format_str = '%d/%m/%y'  # the format in which dates are stored in CSV file
        format_str = '%Y-%m-%d'
        instance.edit_date = datetime.strptime(instance.edit_date, format_str)
        instance.premiere_date = datetime.strptime(instance.premiere_date, format_str)
        print(instance)
        return instance


'''
class EeAttendSummaryResource(resources.ModelResource):
    class Meta:
        model = EeAttendSummary
'''


def excel_set_style(name,height,bold=False):
	style = xlwt.XFStyle()
	font = xlwt.Font()
	font.name = name
	font.bold = bold
	font.color_index = 4
	font.height = height
	style.font = font
	return style