# -*- coding: utf-8 -*-
"""
@Software Platform: PyCharm
@File    : image_storage.py
@Time    : 2020/4/4 0:22
@Author  : 
@Email   : 
@Desc  :
"""
import os
import sys
from fdfs_client.client import Fdfs_client
from fdfs_client.client import get_tracker_conf
import imghdr

config_path = r"E:\Projects\PyCharmProjects\iHome\iHome\utils\FastDFS_image_upload\conf\client.conf"


# print("配置文件绝对路径:", get_config_path())


def upload_image(filename):
    """通过文件的方式上传文件"""
    tracker = get_tracker_conf(conf_path=config_path)
    client = Fdfs_client(trackers=tracker)

    result = client.upload_by_filename(filename=filename)
    # print(result)
    if result.get("Status") != "Upload successed.":
        raise Exception("上传文件失败！")
    res = result.get("Remote file_id")  # group1/M00/00/00/J2phhF6HbbOAWyioACV4d-3-XeU659.jpg
    return res.decode("UTF-8")


# http://39.106.97.132:8888/group1/M00/00/00/J2phhF6HbbOAWyioACV4d-3-XeU659.jpg
def upload_image_by_buffer(file_buffer, file_ext_name=None, meta_dict=None):
    """通过文件流上传文件"""
    print("准备读取配置文件")
    tracker = get_tracker_conf(conf_path=config_path)
    client = Fdfs_client(trackers=tracker)
    print("配置文件读取完成")

    if file_ext_name is None:
        file_ext_name = imghdr.what(file_buffer)  # 判断上传的图片文件格式
        file_buffer = file_buffer.read()  # 注意！FastDFS无法直接读取flask上传的图片，需要经过这一步！！！

    result = client.upload_by_buffer(filebuffer=file_buffer, file_ext_name=file_ext_name, meta_dict=meta_dict)
    print("DFS返回信息：", result)
    if result.get("Status") != "Upload successed.":
        errmsg = "上传文件失败，错误代码：{}".format(result.get("Status"))
        raise Exception(errmsg)

    res = result.get("Remote file_id")  # group1/M00/00/00/J2phhF6HbbOAWyioACV4d-3-XeU659.jpg
    return res.decode("UTF-8")

###################################################################################################
