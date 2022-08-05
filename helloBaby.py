#!/usr/bin/python3
#coding=utf-8
import sys
import json
import requests
import time
from datetime import date, timedelta

class helloBaby:
    # 初始化
    def __init__(self, wechat_config):
        self.appid = wechat_config['appid'].strip()
        self.appsecret = wechat_config['appsecret'].strip()
        self.template_id = wechat_config['template_id'].strip()
        self.access_token = ''

    # 错误代码
    def get_error_info(self, errcode):
        return {
            40013: '不合法的 AppID ，请开发者检查 AppID 的正确性，避免异常字符，注意大小写',
            40125: '无效的appsecret',
            41001: '缺少 access_token 参数',
            40003: '不合法的 OpenID ，请开发者确认 OpenID （该用户）是否已关注公众号，或是否是其他公众号的 OpenID',
            40037: '无效的模板ID',
        }.get(errcode,'unknown error')

    # 打印日志
    def print_log(self, data, openid=''):
        errcode = data['errcode']
        errmsg = data['errmsg']
        if errcode == 0:
            print(' [INFO] send to %s is success' % openid)
        else:
            print(' [ERROR] (%s) %s - %s' % (errcode, errmsg, self.get_error_info(errcode)))
            if openid != '':
                print(' [ERROR] send to %s is error' % openid)
            sys.exit(1)

    # 获取access_token
    def get_access_token(self, appid, appsecret):
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (appid, appsecret)
        r = requests.get(url)
        data = json.loads(r.text)
        if 'errcode' in data:
            self.print_log(data)
        else:
            self.access_token = data['access_token']

    # 获取用户列表
    def get_user_list(self):
        if self.access_token == '':
            self.get_access_token(self.appid, self.appsecret)
        url = 'https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s&next_openid=' % self.access_token
        r = requests.get(url)
        data = json.loads(r.text)
        if 'errcode' in data:
            self.print_log(data)
        else:
            openids = data['data']['openid']
            return openids

    # 发送消息
    #def send_msg(self, openid, template_id, iciba_everyday):
    def send_msg(self, openid, template_id, msgBox):
        msg = {
            'touser': openid,
            'template_id': template_id,
            'url': '',
            'data': {
                'date': {
                    'value': msgBox['date'],
                    'color': '#996600'
                    },
                'helloStr': {
                    'value': msgBox['helloStr'],
                    'color': '#990033'
                    },
                'weatherNow': {
                    'value': msgBox['weatherNow'],
                    'color': '#660066'
                    },
                'tempNow': {
                    'value': msgBox['tempNow'],
                    'color': '#FF3300'
                    },
                'fTemp': {
                    'value': msgBox['fTemp'],
                    'color': '#FF3300'
                    },
                'windNow': {
                    'value': msgBox['windNow'],
                    'color': '#003399'
                    },
                'weatherFc': {
                    'value': msgBox['weatherFc'],
                    'color': '#660066'
                    },
                'tempHigh': {
                    'value': msgBox['tempHigh'],
                    'color': '#FF3300'
                    },
                'tempLow': {
                    'value': msgBox['tempLow'],
                    'color': '#009900'
                    },
                'windDay': {
                    'value': msgBox['windDay'],
                    'color': '#003399'
                    },
                'meetDays': {
                    'value': msgBox['meetDays'],
                    'color': '#FF00CC'
                    },
                'loveDays': {
                    'value': msgBox['loveDays'],
                    'color': '#FF00CC'
                    },
                'merryDays': {
                    'value': msgBox['merryDays'],
                    'color': '#FF00CC'
                    },
                'rainbow': {
                    'value': msgBox['rainbow'],
                    'color': '#CC3366'
                    },
                'cibaEN': {
                    'value': msgBox['cibaEN'],
                    'color': '#3399FF'
                    },
                'cibaCN': {
                    'value': msgBox['cibaCN'],
                    'color': '#336699'
                },                
            }
        }
        json_data = json.dumps(msg)
        if self.access_token == '':
            self.get_access_token(self.appid, self.appsecret)
        url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s' % self.access_token
        r = requests.post(url, json_data)
        return json.loads(r.text)

    # 获取爱词霸每日一句
    def get_iciba_everyday(self):
        url = 'http://open.iciba.com/dsapi/'
        r = requests.get(url)
        return json.loads(r.text)

    # 为设置的用户列表发送消息
    def send_everyday_words(self, openids):
        everyday_words = self.get_iciba_everyday()
        msgBox['cibaEN'] = everyday_words['content']
        msgBox['cibaCN'] = everyday_words['note']
        for openid in openids:
            openid = openid.strip()
            result = self.send_msg(openid, self.template_id, msgBox)
            self.print_log(result, openid)
    
    #获取百度天气
    def getBdWeather(self):
        urlNow = 'https://api.map.baidu.com/weather/v1/?district_id=320100&data_type=now&ak=B66c00e91215573bfa589b26a6da3fc2'
        urlFc = 'https://api.map.baidu.com/weather/v1/?district_id=320100&data_type=fc&ak=B66c00e91215573bfa589b26a6da3fc2'
        #weatherMsg1 = ""
        #weatherMsg2 = ""
        r = requests.get(urlNow)
        data = json.loads(r.text)
        #print(data)
        if data['status'] == 0:
            #weatherMsg1 = "当前天气%s，气温%d℃，体感温度%d℃，%s%s。" % (data['result']['now']['text'],data['result']['now']['temp'],data['result']['now']['feels_like'],data['result']['now']['wind_dir'],data['result']['now']['wind_class'])
            msgBox['weatherNow'] = data['result']['now']['text']
            msgBox['tempNow'] = data['result']['now']['temp']
            msgBox['fTemp'] = data['result']['now']['feels_like']
            msgBox['windNow'] = data['result']['now']['wind_dir'] + data['result']['now']['wind_class']
            #print(msgBox)
        else:
            print(data['message'])

        r = requests.get(urlFc)
        data = json.loads(r.text)
        #print(data)
        if data['status'] == 0:
            #weatherMsg2 = "预计今天天气%s，最高气温%d℃，最低气温%d℃，%s%s。" % (data['result']['forecasts'][0]['text_day'],data['result']['forecasts'][0]['high'],data['result']['forecasts'][0]['low'],data['result']['forecasts'][0]['wd_day'],data['result']['forecasts'][0]['wc_day'])
            msgBox['weatherFc'] = data['result']['forecasts'][0]['text_day']
            msgBox['tempHigh'] = data['result']['forecasts'][0]['high']
            msgBox['tempLow'] = data['result']['forecasts'][0]['low']
            msgBox['windDay'] = data['result']['forecasts'][0]['wd_day'] + data['result']['forecasts'][0]['wc_day']
        else:
            print(data['message'])
        return
    
    #获取彩虹屁
    def getRainbow(self):
        url = 'http://api.tianapi.com/caihongpi/index?key=d7534e78fbabffeb8150bfaf93eeab61'
        r = requests.get(url)
        
        data = json.loads(r.text)
        #print(data)
        if data['code'] == 200:
            msgBox['rainbow'] = data['newslist'][0]['content']
        else:
            msgBox['rainbow'] = '今天没有彩虹屁，我只想说爱你♥。'
        
        #msgBox['rainbow'] = '今天没有彩虹屁，我只想说爱你♥。'
        return
    def calDays(self,day1,day2):

        time_array1 = time.strptime(day1, "%Y-%m-%d")

        timestamp_day1 = int(time.mktime(time_array1))

        time_array2 = time.strptime(day2, "%Y-%m-%d")

        timestamp_day2 = int(time.mktime(time_array2))

        result = (timestamp_day2 - timestamp_day1) // 60 // 60 // 24 + 1

        return result
    #获取日历
    def getCalendar(self):
        todayDate = ''
        dateStr = ''
        dateList = []
        lunaryear=''
        lunarmonth = ''
        lunarday = ''
        cnweekday = ''
        
        url1 = 'http://api.tianapi.com/worldtime/index?key=d7534e78fbabffeb8150bfaf93eeab61&city=北京'
        r1 = requests.get(url1)
        data1 = json.loads(r1.text)
        
        if data1['code'] == 200:
            todayDate = data1['newslist'][0]['strtime'].split(' ')[0]
            dateList = todayDate.split('-')
            url2 = 'http://api.tianapi.com/jiejiari/index?key=d7534e78fbabffeb8150bfaf93eeab61&date=%s' % todayDate
            #url2 = 'http://api.tianapi.com/jiejiari/index?key=d7534e78fbabffeb8150bfaf93eeab61&date=2022-08-04'
            r2 = requests.get(url2)
            data2 = json.loads(r2.text)
            if data2['code'] == 200:
                lunaryear = data2['newslist'][0]['lunaryear']
                lunarmonth = data2['newslist'][0]['lunarmonth']
                lunarday = data2['newslist'][0]['lunarday']
                cnweekday = data2['newslist'][0]['cnweekday']
                #测试日期
                #todayDate = '2022-08-04'
                #print(todayDate.find('10-30',5))
                if todayDate.find('10-30',5) != -1:
                    msgBox['helloStr'] = '生日快乐呦！'
                elif todayDate.find('02-14',5) != -1:
                    msgBox['helloStr'] = '情人节快乐呦！'
                elif lunarmonth == '七月' and lunarday == '初七' :
                    msgBox['helloStr'] = '七夕节快乐呦！'
                else:
                    msgBox['helloStr'] = '今天要开心哟！'
        msgBox['date'] = '%s年%s月%s日（%s年%s%s）%s' % (dateList[0],dateList[1],dateList[2],lunaryear,lunarmonth,lunarday,cnweekday)
        msgBox['meetDays'] = self.calDays('2016-03-12',todayDate)
        msgBox['loveDays'] = self.calDays('2016-05-20',todayDate)
        msgBox['merryDays'] = self.calDays('2017-03-18',todayDate)
        
        return
    # 执行
    def run(self, openids=[]):
        if openids == []:
            # 如果openids为空，则遍历用户列表
            openids = self.get_user_list()
        #获取天气
        self.getBdWeather()
        #获取彩虹屁
        self.getRainbow()
        #获取日历
        self.getCalendar()
        # 根据openids对用户进行群发
        self.send_everyday_words(openids)

if __name__ == '__main__':
    # 微信配置
    wechat_config = {
        'appid': 'wx8a41e021a4056c46', #(No.1)此处填写你的appid
        'appsecret': '7c2d66835775d216e22d9700a9f1046e', #(No.2)此处填写你的appsecret
        'template_id': '7iTo6q6CEp8KplpQp-0arU0HGW-pV4P9sNttR0L8q6w' #(No.3)此处填写你的模板消息ID
    }
    msgBox = {
        'date': '',
        'helloStr': '',
        'weatherNow': '',
        'tempNow': 0,
        'fTemp': 0,
        'windNow': '',
        'weatherFc': '',
        'tempHigh': 0,
        'tempLow': 0,
        'windDay': '',
        'meetDays': 0,
        'loveDays': 0,
        'merryDays': 0,
        'rainbow': '',
        'cibaEN': '',
        'cibaCN':'',
    }
    # 用户列表
    openids = [
        'odxjm5mM7zXFHqXP8gd6LHwGoXWU', #(No.4)此处填写你的微信号（微信公众平台上你的微信号）
        #'xxxxx', #如果有多个用户也可以
        #'xxxxx',
    ]
    # 执行
    hb = helloBaby(wechat_config)
    # run()方法可以传入openids列表，也可不传参数
    # 不传参数则对微信公众号的所有用户进行群发
    hb.run()
    #hb.getCalendar()