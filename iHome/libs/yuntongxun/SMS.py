# -*- coding: UTF-8 -*-

from CCPRestSDK import REST

# import ConfigParser

# 主帐号
accountSid = "8a216da870e2267e01710a4956691464"

# 主帐号Token
accountToken = "d5a20e71c3814bec94f8978cc2abe30e"

# 应用Id
appId = "8a216da870e2267e01710a4956ec146b"

# 请求地址，格式如下，不需要写http://
serverIP = "app.cloopen.com"

# 请求端口
serverPort = 8883

# REST版本号
softVersion = "2013-12-26"


# 发送模板短信
# @param to 手机号码
# @param datas 内容数据 格式为列表 例如：["12","34"]，如不需替换请填 ""
# @param $tempId 模板Id

class CCP(object):
    """用于自己封装的发送短信的辅助类"""
    # 用来保存对象的类属性
    # 单例模式
    instance = None

    def __new__(cls):
        # sendTemplateSMS(手机号码,内容数据,模板Id)

        # 判断CCP类有没有已经创建好的对象，如果没有，创建一个对象，并且保存
        # 如果有，则将保存的对象直接返回
        if cls.instance is None:
            obj = super(CCP, cls).__new__(cls)
            # 初始化REST SDK
            obj.rest = REST(serverIP, serverPort, softVersion)
            obj.rest.setAccount(accountSid, accountToken)
            obj.rest.setAppId(appId)
            cls.instance = obj
            return cls.instance

    def send_template_sms(self, to, datas, temp_id):
        """"""
        result = self.rest.sendTemplateSMS(to, datas, temp_id)
        # for k, v in result.iteritems():
        #
        #     if k == "templateSMS":
        #         for k, s in v.iteritems():
        #             print("%s:%s" % (k, s))
        #     else:
        #         print("%s:%s" % (k, v))

        status_code = result.get("status_code")
        if status_code == "000000":
            # 表示发送短信成功
            return 0
        else:
            # 发送失败
            return -1


if __name__ == '__main__':
    cpp = CCP()
    cpp.send_template_sms(to="15763778971", datas=["1234", 5], temp_id=1)
