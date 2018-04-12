from django.template import Library
from django.utils.safestring import mark_safe

import datetime, time

register = Library()


@register.simple_tag
def build_filter_ele(filter_column, admin_class):
    column_obj = admin_class.model._meta.get_field(filter_column)
    try:
        filter_ele = '<select name=%s>' % filter_column
        for choice in column_obj.get_choices():
            selected = ''
            if filter_column in admin_class.filter_contions:
                if str(choice[0]) == admin_class.filter_contions.get(filter_column):
                    selected = 'selected'

            option = "<option value='%s' %s>%s</option>" % (choice[0], selected, choice[1])
            filter_ele += option

    except ArithmeticError as e:
        print('erro', e)
        filter_ele = '<select name=%s_gte>' % filter_column
        if column_obj.get_internal_type() in ('DateField', 'DateTimeField'):

            time_obj = datetime.datetime.now()
            time_list = [
                ['', '--------'],
                [time_obj, 'Today'],
                [time_obj - datetime.timedelta(7), '七天内'],
                [time_obj.replace(day=1), '本月'],
                [time_obj - datetime.timedelta(90), '三个月内'],
                [time_obj.replace(month=1, day=1), 'YearToday(YID)'],
                ['', 'all']
            ]

            for i in time_list:
                selected = ''
                time_to_str = '' if not i[0] else "%s-%s-%s" % (i[0].year, i[0].month, i[0].day)
                if '%s-gte' % filter_column in admin_class.filter_contions:
                    if time_to_str == admin_class.filter_contions.get('%s-gte' % filter_column):
                        selected = 'selected'

                option = "<option value='%s'%s>%s</option>" % \
                         (time_obj, selected, i[1])
                filter_ele += option
    filter_ele += '</select>'


@register.simple_tag
def build_table_row(obj, admin_class):
    '''生成一条记录的HTML ELEMENT'''
    ele = ''
    if admin_class.list_diaplay:
        for column_name in admin_class.list_diaplay:

            column_obj = admin_class.model._meta.get_field(column_name)
            if column_obj.choices:
                column_data = getattr(obj, 'get_%s_display' % column_name)()
            else:
                column_data = getattr(obj, column_name)
            td_ele = '<td>%s</td>' % column_data
            ele += td_ele
    else:
        td_ele= "<td>%s</td>" % obj
        ele += td_ele
    return mark_safe(ele)


@register.simple_tag
def get_model_name(admin_class):
    return admin_class.model._meta.model_name.upper
@register.simple_tag
def render_paginator(querysets):
        ele ='''
        
          <ul class="pagination">
            

         
        '''
        for i in querysets.paginator.page_range:
            if abs(querysets.number - i)<2:
                active =''
                if querysets.number == i:
                    active ='active'
                p_ele ='''<li class="%s><a href="?_page=%s">%s</a></li>''' % (active,i,i)
                ele +=p_ele
        ele +='</ul>'
        return mark_safe(ele)
