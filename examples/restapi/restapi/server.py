#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from flask import Flask, jsonify
app = Flask(__name__)
import sys
import json
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)
import logging
# local import
from helperfunc import *

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
proc_cpuinfo_file = '/proc/cpuinfo'
proc_meminfo_file = '/proc/meminfo'
http_header = {'Content-Type': 'application/json'}


@app.route('/info/cpu', methods=['GET'])
def info_cpu():
    return proc_cpuinfo_to_json(proc_cpuinfo_file), http_header


@app.route('/info/memory', methods=['GET'])
def info_memory():
    return proc_meminfo_to_json(proc_meminfo_file), http_header


@app.route('/info/fs', methods=['GET'])
def info_fs():
    return df_to_json(), http_header


@app.route('/test/icmp_ping/<ip_addr>/latency', methods=['GET'])
def icmp_ping_latency(ip_addr):
    return icmp_ping_latency_to_json(ip_addr), http_header


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port='8080')
