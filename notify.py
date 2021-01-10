'''
@File    : notify.py
@Time    : 2021-01-10 16:01:53
@Github  : https://github.com/y1ndan/genshin-impact-helper
'''
import json
import os
import requests
import time
import hmac
import hashlib
import base64
from settings import log


class Notify(object):
    @staticmethod
    def to_python(json_str: str):
        return json.loads(json_str)

    @staticmethod
    def to_json(obj):
        return json.dumps(obj, indent=4, ensure_ascii=False)

    # ============================== Server Chan ==============================
    # 此处填你申请的SCKEY
    # 注: Github Actions用户请到Settings->Secrets里设置,Name=PUSH_SCKEY,Value=<获取的值>
    PUSH_SCKEY = 'SCU46297Tf6d9f00f257e60e01ce8abd65a7818fb5c87e7ae8c462'

    if os.environ.get('PUSH_SCKEY', '') != '':
        PUSH_SCKEY = os.environ['PUSH_SCKEY']

    # ============================== Cool Push ================================
    # 此处填你申请的SKEY(详见文档: https://cp.xuthus.cc/)
    # 注: Github Actions用户请到Settings->Secrets里设置,Name=PUSH_SKEY,Value=<获取的值>
    PUSH_SKEY = '0039db7da7a89e2d3d51f3a8a101f34a'
    # 此处填写私聊(send)或群组(group)或者微信(wx)推送方式，默认私聊推送
    # 注: Github Actions用户若要更改,请到Settings->Secrets里设置,Name=PUSH_SKEY_MODE,Value=<group或wx>
    PUSH_SKEY_MODE = 'send'

    if os.environ.get('PUSH_SKEY', '') != '':
        PUSH_SKEY = os.environ['PUSH_SKEY']
    if os.environ.get('PUSH_SKEY_MODE', '') != '':
        PUSH_SKEY_MODE = os.environ['PUSH_SKEY_MODE']

    # ============================== iOS Bark App =============================
    # 此处填你Bark App的信息(IP/设备码,例如: https://api.day.app/XXXXXXXX)
    # 注: Github Actions用户请到Settings->Secrets里设置,Name=PUSH_BARK,Value=<获取的值>
    PUSH_BARK = 'q39t8ZAu9xchgsopHM9Z9F'
    # BARK App推送铃声,铃声列表去App内查看
    # 注: Github Actions用户若要更改,请到Settings->Secrets里设置,Name=PUSH_BARK_SOUND,Value=<铃声名称>
    PUSH_BARK_SOUND = 'healthnotification'

    if os.environ.get('PUSH_BARK', '') != '':
        if os.environ['PUSH_BARK'].find(
                'https') != -1 or os.environ['PUSH_BARK'].find('http') != -1:
            # 兼容BARK自建用户
            PUSH_BARK = os.environ['PUSH_BARK']
        else:
            PUSH_BARK = 'https://api.day.app/' + os.environ['PUSH_BARK']
    elif os.environ.get('PUSH_BARK_SOUND', '') != '':
        PUSH_BARK_SOUND = os.environ['PUSH_BARK_SOUND']
    elif PUSH_BARK != '' or PUSH_BARK.find('https') != -1 or PUSH_BARK.find(
            'http') != -1:
        # 兼容BARK本地用户只填写设备码的情况
        PUSH_BARK = 'https://api.day.app/' + PUSH_BARK

    # ============================== Telegram Bot =============================
    # 此处填你telegram bot的Token,例如: 1077xxx4424:AAFjv0FcqxxxxxxgEMGfi22B4yh15R5uw
    # 注: Github Actions用户请到Settings->Secrets里设置,Name=TG_BOT_TOKEN,Value=<获取的值>
    TG_BOT_TOKEN = '1571428155:AAGMd3aLST6Y55PQwadaqENivlK_70zgERQ'
    # 此处填你接收通知消息的telegram用户的id,例如: 129xxx206
    # 注: Github Actions用户请到Settings->Secrets里设置,Name=TG_USER_ID,Value=<获取的值>
    TG_USER_ID = '370007185'

    if os.environ.get('TG_BOT_TOKEN', '') != '':
        TG_BOT_TOKEN = os.environ['TG_BOT_TOKEN']
    if os.environ.get('TG_USER_ID', '') != '':
        TG_USER_ID = os.environ['TG_USER_ID']

    # ============================== DingTalk Bot =============================
    # 此处填你钉钉机器人的webhook,例如: 5a544165465465645d0f31dca676e7bd07415asdasd
    # 注: Github Actions用户请到Settings->Secrets里设置,Name=DD_BOT_TOKEN,Value=<获取的值>
    DD_BOT_TOKEN = ''
    # 密钥,机器人安全设置页面,加签一栏下面显示的SEC开头的字符串
    # 注: Github Actions用户请到Settings->Secrets里设置,Name=DD_BOT_SECRET,Value=<获取的值>
    DD_BOT_SECRET = ''

    if os.environ.get('DD_BOT_TOKEN', '') != '':
        DD_BOT_TOKEN = os.environ['DD_BOT_TOKEN']
    if os.environ.get('DD_BOT_SECRET', '') != '':
        DD_BOT_SECRET = os.environ['DD_BOT_SECRET']

    # ============================== WeChat Work Bot ==========================
    # 此处填你企业微信机器人的webhook(详见文档 https://work.weixin.qq.com/api/doc/90000/90136/91770) 例如: 693a91f6-7xxx-4bc4-97a0-0ec2sifa5aaa
    # 注: Github Actions用户请到Settings->Secrets里设置,Name=WW_BOT_KEY,Value=<获取的值>
    WW_BOT_KEY = ''

    if os.environ.get('WW_BOT_KEY', '') != '':
        WW_BOT_KEY = os.environ['WW_BOT_KEY']

    # ============================== iGot聚合推送 =================================
    # 此处填你iGot的信息(推送key,例如: https://push.hellyw.com/XXXXXXXX)
    # 注: Github Actions用户请到Settings->Secrets里设置,Name=PUSH_IGOT,Value=<获取的值>
    PUSH_IGOT = '5ff9770a85de28047e335e85'

    if os.environ.get('PUSH_IGOT', '') != '':
        PUSH_IGOT = os.environ['PUSH_IGOT']

    # ============================== push+ ====================================
    # 官方文档: https://pushplus.hxtrip.com/
    # PUSH_PLUS_TOKEN: 微信扫码登录后一对一推送或一对多推送下面的token(您的Token)，不提供PUSH_PLUS_USER则默认为一对一推送
    # 注: Github Actions用户请到Settings->Secrets里设置,Name=PUSH_PLUS_TOKEN,Value=<获取的值>
    PUSH_PLUS_TOKEN = 'd622bc1cf9cc4929a526913d97060bc4'
    # PUSH_PLUS_USER: 一对多推送的“群组编码”（一对多推送下面->您的群组(如无则新建)->群组编码，如果您是创建群组人。也需点击“查看二维码”扫描绑定，否则不能接受群组消息推送）
    # 注: Github Actions用户请到Settings->Secrets里设置,Name=PUSH_PLUS_USER,Value=<获取的值>
    PUSH_PLUS_USER = ''

    if os.environ.get('PUSH_PLUS_TOKEN', '') != '':
        PUSH_PLUS_TOKEN = os.environ['PUSH_PLUS_TOKEN']
    if os.environ.get('PUSH_PLUS_USER', '') != '':
        PUSH_PLUS_USER = os.environ['PUSH_PLUS_USER']

    def serverChan(self, text, status, desp):
        if Notify.PUSH_SCKEY != '':
            url = 'https://sc.ftqq.com/{}.send'.format(Notify.PUSH_SCKEY)
            data = {
                'text': '{} {}'.format(text, status), 
                'desp': desp
            }
            try:
                response = self.to_python(requests.post(url, data=data).text)
            except Exception as e:
                log.error(e)
                raise HTTPError
            else:
                if response['errno'] == 0:
                    log.info('Server酱推送成功')
                elif response['errno'] == 1024:
                    # SCKEY错误或一分钟内发送相同内容
                    log.error('Server酱推送失败:\n{}'.format(response['errmsg']))
                else:
                    log.error('Server酱推送失败:\n{}'.format(response))
        else:
            log.info('您未提供Server酱推送所需的SCKEY,取消Server酱推送通知')
            pass

    def coolPush(self, text, status, desp):
        if Notify.PUSH_SKEY != '':
            url = 'https://push.xuthus.cc/{}/{}'.format(
                Notify.PUSH_SKEY_MODE, Notify.PUSH_SKEY)
            data = '{} {}\n\n{}'.format(text, status, desp).encode('utf-8')
            try:
                response = self.to_python(requests.post(url, data=data).text)
            except Exception as e:
                log.error(e)
                raise HTTPError
            else:
                if response['code'] == 200:
                    log.info('Cool Push推送成功')
                else:
                    log.error('Cool Push推送失败:\n{}'.format(response))
        else:
            log.info('您未提供酷推推送所需的SKEY,取消酷推推送通知')
            pass

    def bark(self, text, status, desp):
        if Notify.PUSH_BARK != '':
            url = '{}/{} {}/{}?sound={}'.format(Notify.PUSH_BARK, text, status,
                desp, Notify.PUSH_BARK_SOUND)
            try:
                response = self.to_python(requests.get(url).text)
            except Exception as e:
                log.error(e)
                raise HTTPError
            else:
                if response['code'] == 200:
                    log.info('Bark推送成功')
                elif response['code'] == 400:
                    log.error('Bark推送失败:\n{}'.format(response['message']))
                else:
                    log.error('Bark推送失败:\n{}'.format(response))
        else:
            log.info('您未提供Bark推送所需的PUSH_BARK,取消Bark推送通知')
            pass

    def tgBot(self, text, status, desp):
        if Notify.TG_BOT_TOKEN != '' or Notify.TG_USER_ID != '':
            url = 'https://api.telegram.org/bot{}/sendMessage'.format(
                Notify.TG_BOT_TOKEN)
            data = {
                'chat_id': Notify.TG_USER_ID,
                'text': '{} {}\n\n{}'.format(text, status, desp),
                'disable_web_page_preview': True
            }
            try:
                response = self.to_python(requests.post(url, data=data).text)
            except Exception as e:
                log.error(e)
                raise HTTPError
            else:
                if response['ok'] == True:
                    log.info('Telegram推送成功')
                elif response['error_code'] == 400:
                    log.error('请主动给bot发送一条消息并检查接收用户ID是否正确')
                elif response['error_code'] == 401:
                    log.error('TG_BOT_TOKEN错误')
                else:
                    log.error('Telegram推送失败:\n{}'.format(response))
        else:
            log.info(
                '您未提供Telegram Bot推送所需的TG_BOT_TOKEN和TG_USER_ID,取消Telegram推送通知')
            pass

    def ddBot(self, text, status, desp):
        if Notify.DD_BOT_TOKEN != '':
            url = 'https://oapi.dingtalk.com/robot/send?access_token={}'.format(
                Notify.DD_BOT_TOKEN)
            data = {
                'msgtype': 'text',
                'text': {
                    'content': '{} {}\n\n{}'.format(text, status, desp)
                }
            }
            if Notify.DD_BOT_SECRET != '':
                timestamp = long(round(time.time() * 1000))
                secret_enc = bytes(secret).encode('utf-8')
                string_to_sign = '{}\n{}'.format(timestamp, secret)
                string_to_sign_enc = bytes(string_to_sign).encode('utf-8')
                hmac_code = hmac.new(
                    secret_enc, string_to_sign_enc,
                    digestmod=hashlib.sha256).digest()
                sign = urllib.quote_plus(base64.b64encode(hmac_code))
                url = 'https://oapi.dingtalk.com/robot/send?access_token={}&timestamp={}&sign={}'.format(
                    Notify.DD_BOT_TOKEN, timestamp, sign)
            try:
                response = self.to_python(requests.post(url, data=data).text)
            except Exception as e:
                log.error(e)
                raise HTTPError
            else:
                if response['errcode'] == 0:
                    log.info('钉钉推送成功')
                else:
                    log.error('钉钉推送失败:\n{}'.format(response))
        else:
            log.info('您未提供钉钉推送所需的DD_BOT_TOKEN或DD_BOT_SECRET,取消钉钉推送通知')
            pass

    def wwBot(self, text, status, desp):
        if Notify.WW_BOT_TOKEN != '':
            url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={}'.format(Notify.WW_BOT_TOKEN)
            data = {
                'msgtype': 'text',
                'text': {
                    'content': '{} {}\n\n{}'.format(text, status, desp)
                }
            }
            try:
                response = self.to_python(requests.post(url, data=data).text)
            except Exception as e:
                log.error(e)
                raise HTTPError
            else:
                if response['errcode'] == 0:
                    log.info('企业微信推送成功')
                else:
                    log.error('企业微信推送失败:\n{}'.format(response))
        else:
            log.info('您未提供企业微信推送所需的WW_BOT_TOKEN,取消企业微信推送通知')
            pass

    def iGot(self, text, status, desp):
        if Notify.PUSH_IGOT != '':
            url = 'https://push.hellyw.com/{}'.format(Notify.PUSH_IGOT)
            data = {
                'title': '{} {}'.format(text, status),
                'content': desp
            }
            try:
                response = self.to_python(requests.post(url, data=data).text)
            except Exception as e:
                log.error(e)
                raise HTTPError
            else:
                if response['ret'] == 0:
                    log.info('iGot推送成功')
                else:
                    log.error('iGot推送失败:\n{}'.format(response))
        else:
            log.info('您未提供iGot推送所需的PUSH_IGOT,取消iGot推送通知')
            pass

    def pushPlus(self, text, status, desp):
        if Notify.PUSH_PLUS_TOKEN != '':
            url = 'https://pushplus.hxtrip.com/send'
            data = {
                'token': Notify.PUSH_PLUS_TOKEN,
                'title': '{} {}'.format(text, status),
                'content': desp,
                'topic': Notify.PUSH_PLUS_USER
            }
            try:
                response = self.to_python(requests.post(url, data=data).text)
            except Exception as e:
                log.error(e)
                raise HTTPError
            else:
                if response['code'] == 200:
                    log.info('pushplus推送成功')
                else:
                    log.error('pushplus推送失败:\n{}'.format(response))
        else:
            log.info('您未提供pushplus推送所需的PUSH_PLUS_TOKEN,取消pushplus推送通知')
            pass

    def send(self, **kwargs):
        log.info('准备推送通知...')
        app = kwargs.get('app', '')
        status = kwargs.get('status', '')
        msg = kwargs.get('msg', '')

        #self.serverChan(app, status, msg)
        #self.coolPush(app, status, msg)
        self.bark(app, status, msg)
        #self.tgBot(app, status, msg)
        #self.ddBot(app, status, msg)
        #self.wwBot(app, status, msg)
        #self.iGot(app, status, msg)
        #self.pushPlus(app, status, msg)


if __name__ == '__main__':
    Notify().send(app='原神签到小助手', status='签到状态', msg='内容详情')

