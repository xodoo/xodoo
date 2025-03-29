# -*- coding: utf-8 -*-
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# odoo18
# QQ:35350428
# 邮件:35350428@qq.com
# 手机：13584935775
# 作者：'Amos'
# 公司网址： www.xodoo.cn
# Copyright 昆山一百计算机有限公司
# 日期：2023-09-16
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

import calendar
from pytz import timezone, UTC, utc
import pytz
from odoo import models, fields
from collections import defaultdict
from datetime import datetime, time, timedelta
from pytz import timezone, utc
from dateutil.relativedelta import relativedelta
from odoo.tools.misc import get_lang

"""
引入：from odoo import tools
调用方式如下
dates = tools.jinja_date._get_first_last_day(type="下半年")
# 反转列表以倒序返回
dates.reverse()
for i, (start, end) in enumerate(dates):
    date_start = start.strftime('%Y-%m-%d')
    date_end = end.strftime('%Y-%m-%d')
    print(date_start, date_end)
"""


# TODO(amos): 返回天日期时间
def _get_date_range(type='', value=''):
    """
    返回当前时间所在月的天数,返回指定日期月所有的天数
    :param type: 类型
    :param value: 提供日期
    """

    if type == '今天' or type == '':
        """
        tools.jinja_date._get_date_range(type="今天")
        结束：
        {'start_time': datetime.datetime(2024, 11, 23, 0, 0), 'end_time': datetime.datetime(2024, 11, 23, 23, 59, 59, 999999)}
        """
        # 获取今天的日期
        today = datetime.now().date()
        # 计算今天的开始时间（00:00:00）
        start_time = datetime.combine(today, time.min)
        # 计算今天的结束时间（23:59:59）
        end_time = datetime.combine(today, time.max)

        # print(f"开始时间（格式化）：{start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        # print(f"结束时间（格式化）：{end_time.strftime('%Y-%m-%d %H:%M:%S')}")

        values = {
            'start_time': start_time,
            'end_time': end_time,
        }
        return values
    elif type == '昨天':
        """
        tools.jinja_date._get_date_range(type="昨天")
        结束：
        {'start_time': datetime.datetime(2024, 11, 22, 0, 0), 'end_time': datetime.datetime(2024, 11, 22, 23, 59, 59, 999999)}
        """
        # 获取昨天的日期
        yesterday = datetime.now().date() - timedelta(days=1)
        # 计算昨天的开始时间（00:00:00）
        start_time = datetime.combine(yesterday, time.min)
        # 计算昨天的结束时间（23:59:59）
        end_time = datetime.combine(yesterday, time.max)

        # 如果你需要特定格式的字符串，可以使用 strftime 方法
        # print(f"开始时间（格式化）：{start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        # print(f"结束时间（格式化）：{end_time.strftime('%Y-%m-%d %H:%M:%S')}")

        values = {
            'start_time': start_time,
            'end_time': end_time,
        }
        return values
    elif type == '本月':
        """
        tools.jinja_date._get_date_range(type="本月")
        结束：
        {'start_time': datetime.datetime(2024, 11, 1, 0, 0), 'end_time': datetime.datetime(2024, 11, 30, 23, 59, 59, 999999)}
        """
        # 获取当前年份和月份
        year, month = datetime.today().year, datetime.today().month
        # 获取当月的天数
        days_in_month = calendar.monthrange(year, month)[1]
        # 本月的开始时间（第一天凌晨时间）
        start_time = datetime(year, month, 1)
        # 本月的结束时间（最后一天最后一刻）
        end_time = datetime(year, month, days_in_month) + timedelta(days=1) - timedelta(microseconds=1)
        # 如果需要考虑时区，可以使用pytz库来处理时区问题
        # from pytz import timezone
        # start_time = start_time.replace(tzinfo=timezone('Asia/Shanghai'))
        # end_time = end_time.replace(tzinfo=timezone('Asia/Shanghai'))
        values = {
            'start_time': start_time,
            'end_time': end_time,
        }
        return values
    elif type == '本月每天':
        """
        tools.jinja_date._get_date_range(type="本月每天")
        结束：
        日期：2024-11-01，开始时间：2024-11-01 00:00:00，结束时间：2024-11-01 23:59:59
        ...
        日期：2024-11-29，开始时间：2024-11-29 00:00:00，结束时间：2024-11-29 23:59:59
        """
        day_list = []
        # 获取本月的开始日期
        start_date = datetime.today().replace(day=1)
        # 获取本月的结束日期
        end_date = start_date.replace(month=start_date.month % 12 + 1) - timedelta(days=1)
        # 遍历本月的每一天
        for day in range(0, end_date.day + 1):
            if day == end_date.day:
                day = end_date.day
            else:
                day = day+1
            # 每天的开始时间（凌晨时间）
            start_time = datetime(start_date.year, start_date.month, day)
            # 每天的结束时间（最后一秒）
            end_time = start_time.replace(day=day) - timedelta(seconds=1)
            # print(f"日期：{start_time.date()}，开始时间：{start_time}，结束时间：{end_time}")
            day_list.append((start_time, end_time))
        return day_list
    # elif type == '本月每天':
    #     """
    #     tools.jinja_date._get_date_range(type="本月每天")
    #     结束：
    #     日期：2024-11-01，开始时间：2024-11-01 00:00:00，结束时间：2024-11-01 23:59:59
    #     ...
    #     日期：2024-11-29，开始时间：2024-11-29 00:00:00，结束时间：2024-11-29 23:59:59
    #     """
    #     day_list = []
    #     # 获取本月的开始日期
    #     start_date = datetime.today().replace(day=1)
    #     # 获取本月的结束日期
    #     end_date = start_date.replace(month=start_date.month % 12 + 1) - timedelta(days=1)
    #     # 遍历本月的每一天
    #     for day in range(1, end_date.day + 1):
    #         # 每天的开始时间（凌晨时间）
    #         start_time = datetime(start_date.year, start_date.month, day)
    #         # 每天的结束时间（最后一秒）
    #         end_time = start_time.replace(day=day + 1) - timedelta(seconds=1)
    #         # print(f"日期：{start_time.date()}，开始时间：{start_time}，结束时间：{end_time}")
    #         day_list.append((start_time, end_time))
        return months_range
    elif type == '上月':
        """
        tools.jinja_date._get_date_range(type="本月")
        结束：
        {'start_time': datetime.datetime(2024, 10, 1, 0, 0), 'end_time': datetime.datetime(2024, 10, 30, 23, 59, 59)}
        """
        # 获取当前年份和月份
        year, month = datetime.today().year, datetime.today().month

        # 如果当前月份为1，则上一年度为12月，否则减1
        if month == 1:
            last_month_year = year - 1
            last_month = 12
        else:
            last_month_year = year
            last_month = month - 1

        # 获取上月的天数
        days_in_last_month = calendar.monthrange(last_month_year, last_month)[1]

        # 上月的开始时间（第一天的凌晨时间）
        start_time = datetime(last_month_year, last_month, 1)

        # 上月的结束时间（最后一天的最后一秒）
        end_time = datetime(last_month_year, last_month, days_in_last_month) + timedelta(seconds=-1)

        # 如果需要考虑时区，可以使用pytz库来处理时区问题
        # from pytz import timezone
        # start_time = start_time.replace(tzinfo=timezone('Asia/Shanghai'))
        # end_time = end_time.replace(tzinfo=timezone('Asia/Shanghai'))

        # print("上月的开始时间:", start_time)
        # print("上月的结束日期:", end_time)
        values = {
            'start_time': start_time,
            'end_time': end_time,
        }
        return values
    elif type == '上月每天':
        """
        tools.jinja_date._get_date_range(type="上月每天")
        结束：
        日期：2024-09-01，开始时间：2024-09-01 00:00:00，结束时间：2024-09-01 23:59:59
        ...
        日期：2024-09-29，开始时间：2024-09-29 00:00:00，结束时间：2024-09-29 23:59:59
        """
        day_list = []
        # 获取上个月的开始日期
        start_date = datetime.today().replace(day=1) - timedelta(days=1)
        print("-----")
        print(start_date)
        # 如果当前月份为1，则上一年度为12月，否则减1
        if start_date.month == 1:
            last_month_year = start_date.year - 1
            last_month = 12
        else:
            last_month_year = start_date.year
            last_month = start_date.month
        # 重新计算上个月的开始日期
        start_date = datetime(last_month_year, last_month, 1)
        # 获取上个月的结束日期
        end_date = datetime(last_month_year, last_month, calendar.monthrange(last_month_year, last_month)[1])
        # 遍历上个月的每一天
        for day in range(0, end_date.day+1):
            if day == end_date.day:
                day = end_date.day
            else:
                day = day+1
            # 每天的开始时间（凌晨时间）
            start_time = datetime(start_date.year, start_date.month, day)
            # 每天的结束时间（最后一秒）
            end_time = start_time.replace(day=day) - timedelta(seconds=1)
            print(f"日期：{start_time.date()}，开始时间：{start_time}，结束时间：{end_time}")
            day_list.append((start_time, end_time))
        return day_list

# TODO(amos): 返回当前时间所在月的天数,返回指定日期月所有的天数
def _get_month_date(value=''):
    """
    返回当前时间所在月的天数,返回指定日期月所有的天数
    :param value: 为空：当月有多少天
    :param value: 为日期，指定月的天数
    """

    if value:
        """
        month_dates = tools.jinja_date._get_month_date('2010-12-05')
        结束:
        {'year': 2010, 'month': 12, 'num_days': 31}
        """
        now = datetime.strptime(value, "%Y-%m-%d").date()
        _, num_days = calendar.monthrange(now.year, now.month)
        # print(f"{now.year}年{now.month}月有{num_days}天")

        values = {
            'year': now.year,
            'month': now.month,
            'num_days': num_days,
        }
        return values
    else:
        """
        month_dates = tools.jinja_date._get_month_date("")
        结束:
        {'year': 2024, 'month': 11, 'num_days': 30}
        """
        # 获取当前日期
        now = datetime.now()
        # 获取当前月份的天数
        _, num_days = calendar.monthrange(now.year, now.month)
        # print(f"{now.year}年{now.month}月有{num_days}天")
        values = {
            'year': now.year,
            'month': now.month,
            'num_days': num_days,
        }
        return values


# TODO(amos): 返回指定月的第一天日期与最后一天日期
def _get_first_last_day(type='', number=1, data=''):
    import datetime
    """
    返回指定月的第一天日期与最后一天日期
    :param type: 本月
    :param type: 上月
    :param type: 返回过去月
    :param type: 季度 返回指定年份 季度时间
    :param date: 指定开始日期
    """
    month_day = []

    if type == '本月' or type == '':
        """
        tools.jinja_date._get_first_last_day("本月")
        结束:
        2024-11-01 2024-11-30
        """
        months_range = []
        current_date = datetime.datetime.now()
        # 计算月份的开始时间
        month_start = current_date.replace(day=1) - relativedelta(months=0)
        # 计算月份的结束时间
        # 通过下个月的第0天来获取当前月的最后一天
        month_end = (month_start + relativedelta(months=1)).replace(day=1) - relativedelta(days=1)
        months_range.append((month_start, month_end))
        return months_range

    elif type == '上月':
        """
        tools.jinja_date._get_first_last_day("上月")
        结束:
        2024-10-01 2024-10-31
        """
        months_range = []
        current_date = datetime.datetime.now()
        # 计算月份的开始时间
        month_start = current_date.replace(day=1) - relativedelta(months=1)
        # 计算月份的结束时间
        # 通过下个月的第0天来获取当前月的最后一天
        month_end = (month_start + relativedelta(months=1)).replace(day=1) - relativedelta(days=1)
        months_range.append((month_start, month_end))
        return months_range
    elif type == '本周':
        """
        tools.jinja_date._get_first_last_day(type="本周")
        结束:
        2024-11-18 2024-11-24
        """
        weeks_range = []
        now = datetime.datetime.now()
        this_week_start = now - timedelta(days=now.weekday())
        this_week_end = now + timedelta(days=6 - now.weekday())
        weeks_range.append((this_week_start, this_week_end))
        return weeks_range
    elif type == '上周':
        """
        tools.jinja_date._get_first_last_day(type="上周")
        结束:
        2024-11-11 2024-11-17
        """
        weeks_range = []
        now = datetime.datetime.now()
        last_week_start = now - timedelta(days=now.weekday() + 7)
        last_week_end = now - timedelta(days=now.weekday() + 1)
        weeks_range.append((last_week_start, last_week_end))
        return weeks_range
    elif type == '本年':
        """
        tools.jinja_date._get_first_last_day(type="本年")
        结束:
        2024-01-01 2024-12-31
        """
        year_range = []
        now = datetime.datetime.now()
        this_year_start = datetime.datetime(now.year, 1, 1)
        this_year_end = datetime.datetime(now.year + 1, 1, 1) - timedelta(days=1)
        year_range.append((this_year_start, this_year_end))
        return year_range
    elif type == '去年':
        """
        tools.jinja_date._get_first_last_day(type="去年")
        结束:
        2023-01-01 2023-12-31
        """
        year_range = []
        today = datetime.date.today()
        last_year = today.year - 1
        # 计算去年的开始日期
        last_year_start_date = datetime.date(last_year, 1, 1)
        # 计算去年的结束日期（今年的1月1日减去一天）
        this_year_start_date = datetime.date(today.year, 1, 1)
        last_year_end_date = this_year_start_date - datetime.timedelta(days=1)
        year_range.append((last_year_start_date, last_year_end_date))
        return year_range
    elif type == '今年上半年':
        """
        tools.jinja_date._get_first_last_day(type="今年上半年")
        结束:
        2024-01-01 2024-06-30
        """
        year_range = []

        today = datetime.date.today()
        year = today.year

        # 计算上半年的开始日期
        first_half_start_date = datetime.date(year, 1, 1)
        # 计算上半年的结束日期（下半年的开始日期减去一天）
        second_half_start_date = datetime.date(year, 7, 1)
        first_half_end_date = second_half_start_date - datetime.timedelta(days=1)
        year_range.append((first_half_start_date, first_half_end_date))
        return year_range
    elif type == '今天下半年':
        """
        tools.jinja_date._get_first_last_day(type="今天下半年")
        结束:
        2024-07-01 2024-12-31
        """
        import datetime
        year_range = []

        today = datetime.date.today()
        year = today.year
        # 计算下半年的开始日期
        second_half_start_date = datetime.date(year, 7, 1)
        # 计算下半年的结束日期（下一年的1月1日减去一天）
        next_year_start_date = datetime.date(year + 1, 1, 1)
        second_half_end_date = next_year_start_date - datetime.timedelta(days=1)
        year_range.append((second_half_start_date, second_half_end_date))
        return year_range
    elif type == '本季':
        """
        date_list = tools.jinja_date._get_first_last_day(type="本季")
        # 反转列表以倒序返回
        date_list.reverse()
        for i, (start, end) in enumerate(date_list):
            date_start = start.strftime('%Y-%m-%d')
            date_end = end.strftime('%Y-%m-%d')
            print(date_start, date_end)
        结束:
        2024-10-01 2024-12-31
        """
        quarter_range = []
        today = datetime.date.today()
        current_month = today.month

        # 确定当前季度
        if 1 <= current_month <= 3:
            quarter_start_month = 1
        elif 4 <= current_month <= 6:
            quarter_start_month = 4
        elif 7 <= current_month <= 9:
            quarter_start_month = 7
        else:
            quarter_start_month = 10

        # 计算季度的第一天和最后一天
        year = today.year
        quarter_start_date = datetime.date(year, quarter_start_month, 1)
        if quarter_start_month == 10:
            next_quarter_start_date = datetime.date(year + 1, 1, 1)
        else:
            next_quarter_start_date = datetime.date(year, quarter_start_month + 3, 1)
        quarter_end_date = next_quarter_start_date - datetime.timedelta(days=1)

        quarter_range.append((quarter_start_date, quarter_end_date))
        return quarter_range
    elif type == '返回过去月':
        """
        tools.jinja_date._get_first_last_day("返回过去月",number=6)
        过去6个月，月初与月未时间
        结束:
        2024-06-01 2024-06-30
        2024-07-01 2024-07-31
        2024-08-01 2024-08-31
        2024-09-01 2024-09-30
        2024-10-01 2024-10-31
        2024-11-01 2024-11-30
        """
        # 获取当前日期
        date = datetime.datetime.now()
        # 或者你可以手动设置一个日期，用于测试跨年的情况
        # current_date = datetime(2023, 1, 15)  # 例如，设置为2023年1月15日
        # 初始化一个列表来存储每个月的开始和结束时间
        months_range = []
        # 循环计算过去6个月的开始和结束时间
        for i in range(number):
            # 计算月份的开始时间
            month_start = date.replace(day=1) - relativedelta(months=i)
            # 计算月份的结束时间
            # 通过下个月的第0天来获取当前月的最后一天
            month_end = (month_start + relativedelta(months=1)).replace(day=1) - relativedelta(days=1)
            # 将结果添加到列表中
            months_range.append((month_start, month_end))
        return months_range

    elif type == '指定开始日期':
        """
        tools.jinja_date._get_first_last_day("指定开始日期",number=4,data='2010-12-05')
        结束:
        2010-09-01 2010-09-30
        2010-10-01 2010-10-31
        2010-11-01 2010-11-30
        2010-12-01 2010-12-31
        """
        # 获取当前日期
        date = datetime.datetime.strptime(data, "%Y-%m-%d")
        # 或者你可以手动设置一个日期，用于测试跨年的情况
        # date = datetime(2010, 12, 05)  # 例如，设置为2023年1月15日
        # 初始化一个列表来存储每个月的开始和结束时间
        months_range = []
        # 循环计算过去6个月的开始和结束时间
        for i in range(number):
            # 计算月份的开始时间
            month_start = date.replace(day=1) - relativedelta(months=i)
            # 计算月份的结束时间
            # 通过下个月的第0天来获取当前月的最后一天
            month_end = (month_start + relativedelta(months=1)).replace(day=1) - relativedelta(days=1)
            # 将结果添加到列表中
            months_range.append((month_start, month_end))
        return months_range

    return month_day


# TODO(amos): 返回指定年的季度开始日期与结束日期
def _get_quarter_first_last_day(number=1, data=''):
    """
    返回指定年的季度开始日期与结束日期
    :param number: 【1，2，3，4】第几季度，0 全部季度
    :param date: 指定开始日期
    """
    quarter_list = []
    # number=’‘ 返回指定季度, data='2024' 年份如
    year = datetime.now().year
    if data:
        year = int(data)
    if number == 1:
        """
        tools.jinja_date._get_quarter_first_last_day(number=1)
        如果不指定年份就是当年 一季度
        结束:
        2024-01-01 2024-03-31
        """
        start_date = datetime(year, 1, 1)
        end_date = datetime(year, 4, 1) - timedelta(days=1)
        quarter_list.append((start_date, end_date))
        return quarter_list
    elif number == 2:
        """
        tools.jinja_date._get_quarter_first_last_day(number=1)
        如果不指定年份就是当年 二季度
        结束:
        2024-04-01 2024-06-30
        """
        start_date = datetime(year, 4, 1)
        end_date = datetime(year, 7, 1) - timedelta(days=1)
        quarter_list.append((start_date, end_date))
        return quarter_list
    elif number == 3:
        """
        tools.jinja_date._get_quarter_first_last_day(number=1)
        如果不指定年份就是当年 三季度
        结束:
        2024-07-01 2024-09-30
        """
        start_date = datetime(year, 7, 1)
        end_date = datetime(year, 10, 1) - timedelta(days=1)
        quarter_list.append((start_date, end_date))
        return quarter_list
    elif number == 4:
        """
        tools.jinja_date._get_quarter_first_last_day(number=1)
        如果不指定年份就是当年 四季度
        结束:
        2024-10-01 2024-12-31
        """
        start_date = datetime(year, 10, 1)
        end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
        quarter_list.append((start_date, end_date))
        return quarter_list
    else:
        """
        tools.jinja_date._get_quarter_first_last_day(number=0,data='2010')
        结束:
        2010-10-01 2010-12-31
        2010-07-01 2010-09-30
        2010-04-01 2010-06-30
        2010-01-01 2010-03-31
        """
        for i in range(4):
            start_date = None
            end_date = None
            if i == 0:
                start_date = datetime(year, 1, 1)
                end_date = datetime(year, 4, 1) - timedelta(days=1)
            elif i == 1:
                start_date = datetime(year, 4, 1)
                end_date = datetime(year, 7, 1) - timedelta(days=1)
            elif i == 2:
                start_date = datetime(year, 7, 1)
                end_date = datetime(year, 10, 1) - timedelta(days=1)
            elif i == 3:
                start_date = datetime(year, 10, 1)
                end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
            quarter_list.append((start_date, end_date))
        return quarter_list

    return quarter_list


# TODO(amos): 返回周的开始与结束时间
def _get_weeks_first_last_day(num_weeks=6):
    """
    返回当前日期的最近几周
    :param number:默认返回6周
    """
    """
    weeks_list = tools.jinja_date._get_weeks_first_last_day(6)
    # 获取最近6周的日期
    for week_number, start, end in weeks_list:
        print(f"第{week_number}周: {start.strftime('%Y-%m-%d')} 到 {end.strftime('%Y-%m-%d')}")
    结束：
    第42周: 2024-10-14 到 2024-10-20
    第43周: 2024-10-21 到 2024-10-27
    第44周: 2024-10-28 到 2024-11-03
    第45周: 2024-11-04 到 2024-11-10
    第46周: 2024-11-11 到 2024-11-17
    第47周: 2024-11-18 到 2024-11-24
    """
    today = datetime.now().date()
    # 计算当前周的开始（周一）和结束（周日）
    start_of_current_week = today - timedelta(days=today.weekday())
    end_of_current_week = start_of_current_week + timedelta(days=6)
    # 计算当前是一年中的第几周
    current_week_number = today.isocalendar()[1]
    weeks = []
    for i in range(num_weeks):
        week_start = start_of_current_week - timedelta(weeks=i)
        week_end = end_of_current_week - timedelta(weeks=i)
        week_number = (current_week_number - i) if (current_week_number - i) > 0 else 52 + (current_week_number - i)
        weeks.append((week_number, week_start, week_end))
    return weeks[::-1]
