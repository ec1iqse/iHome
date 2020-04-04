# -*- coding: utf-8 -*-
"""
@Software Platform: PyCharm
@File    : image_storage.py
@Time    : 2020/4/4 0:22
@Author  : 
@Email   : 
@Desc  :
"""
from fdfs_client.client import Fdfs_client
from fdfs_client.client import get_tracker_conf

# tracker = get_tracker_conf("./conf/client.conf")
# client = Fdfs_client(trackers=tracker)
# ret = client.upload_by_filename(filename="./images/fruit.jpg")
# print(ret)

tracker = get_tracker_conf("./conf/client.conf")
client = Fdfs_client(trackers=tracker)


def upload_image(filename):
    result = client.upload_by_filename(filename=filename)
    # print(result)
    if result.get('Status') != 'Upload successed.':
        raise Exception('上传文件失败！')
    res = result.get('Remote file_id')  # group1/M00/00/00/J2phhF6HbbOAWyioACV4d-3-XeU659.jpg
    return res.decode("UTF-8")


# http://39.106.97.132:8888/group1/M00/00/00/J2phhF6HbbOAWyioACV4d-3-XeU659.jpg
def upload_image_by_buffer(filebuffer, file_ext_name=None, meta_dict=None):
    result = client.upload_by_buffer(filebuffer=filebuffer, file_ext_name=file_ext_name, meta_dict=meta_dict)
    # print(result)
    if result.get('Status') != 'Upload successed.':
        raise Exception('上传文件失败！')
    res = result.get('Remote file_id')  # group1/M00/00/00/J2phhF6HbbOAWyioACV4d-3-XeU659.jpg
    return res.decode("UTF-8")
