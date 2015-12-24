#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""通过 ping 命令找出ip
支持 windows，unix，linux
"""

import re
import os
import subprocess
import sys


def ping_domain(str_domain):
    """
    执行ping命令
    """

    str_ip = ''
    if not str_domain:
        return str_ip

    # 系统平台
    os_name = os.name

    # 根据系统平台设置 ping 命令
    if os_name == 'nt':  # windows
        cmd = 'ping ' + str_domain
    else:  # unix/linux
        cmd = 'ping -c 2 ' + str_domain

    # 执行 ping 命令
    sub = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, shell=True)
    out = sub.communicate()[0]
    if not out:
        return str_ip

    # 替换换行符，因为在正则表达式中
    # 'a$' 匹配 'a\r\n' 中的 'a\r'
    text = out.replace('\r\n', '\n').replace('\r', '\n')

    # print text

    # 使用正则匹配 ip 地址: [192.168.1.1] (192.168.1.1)
    ip = re.findall(r'(?<=\(|\[)\d+\.\d+\.\d+\.\d+(?=\)|\])', text)


    # print ip
    if ip:
        str_ip = ip[0]

    return str_ip


def get_domains(file_name):
    """
    从文件中读取 ip/域名
    返回 ip/域名 列表，默认值为空
    """
    domains = []
    with open(file_name) as f:
        for line in f:
            line = line.strip().strip('.,/\n\r')
            if line:
                domains.append(line)
    return domains



if __name__ == '__main__':
    # 处理命令行参数
    argvs = sys.argv
    if len(argvs) < 3:
        print "please use: python domain2ip.py input_domain_list.txt output_ip_list.txt"
        exit(1)

    domains = get_domains(argvs[1])

    for line in domains:
        try:
            print line
            str_ip = ping_domain(line)
            print str_ip
            if str_ip:
                with open(argvs[2], 'a+') as f:
                    f.write(str_ip+ '\n')
        except Exception as e:
            print e
            pass
    exit(0)
