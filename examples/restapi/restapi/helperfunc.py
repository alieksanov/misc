#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import io
import logging
import sys
import subprocess
import re

#proc_cpuinfo_file = '/proc/cpuinfo'
#proc_meminfo_file = '/proc/meminfo'
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


def file_lines_to_array(fname):
    with io.open(fname, 'r') as fh:
        return fh.readlines()


def proc_cpuinfo_to_json(fname):
    cpu_id = 0
    cpu_list = []
    cpu_spec = {}
    for l in file_lines_to_array(fname):
        if l.strip():
            k, v = l.strip().split(':')
            cpu_spec[k.strip()] = v.strip()
        else:
            cpu_list.append(cpu_spec)
    j = json.dumps(cpu_list, indent=4, sort_keys=True)
    return j


def proc_meminfo_to_json(fname):
    mem_list = []
    mem_spec = {}
    for l in file_lines_to_array(fname):
        if not l.strip():
            continue
        k, v = l.strip().split(':')
        #logging.debug('k: {0}\tv: {1}'.format(k.strip(), v.strip()))
        mem_spec[k.strip()] = v.strip()
    mem_list.append(mem_spec)
    j = json.dumps(mem_list, indent=4, sort_keys=True)
    return j


def df_to_json():
    df_list = []
    for i, v in enumerate(subprocess.check_output(['df']).splitlines()):
        fs = {}
        if i == 0:
            keys = re.split(r'\s+', v)
            continue
        values = re.split(r'\s+', v)
        for i2, v2 in enumerate(values):
            fs[keys[i2]] = v2
        df_list.append(fs)
    j = json.dumps(df_list, indent=4, sort_keys=True)
    return j


def icmp_ping_latency_to_json(ip_addr, count='2'):
    avg_latency = '0.0'
    has_error = True
    cmd = ['ping', '-c' + count, '-i0.1', '-q', ip_addr]
    regex = r'(\d+\.\d+)\/(\d+\.\d+)\/(\d+\.\d+)\/(\d+\.\d+)\s+ms'
    try:
        out = subprocess.check_output(cmd)
    except subprocess.CalledProcessError, err:
        logging.error(err)
        match = None
    else:
        match = re.search(regex, out)
    if match:
        avg_latency = match.group(2)
        has_error = False
    j = json.dumps([{'ip_addr': ip_addr,
                    'has_error': has_error,
                    'avg_latency': avg_latency + 'ms',
                    'pkt_count': count}])
    return j

#print(icmp_ping_latency_to_json("8.8.8.8"))
#print(proc_meminfo_to_json(proc_meminfo_file))
#logging.debug(df_to_json())
