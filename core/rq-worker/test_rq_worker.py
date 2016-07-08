import os
import pytest
import subprocess

import file_watch

def test_settings():
    """ Tests settings """
    os.environ['REMOTE_REDIS_HOST'] = "test"
    os.environ['REMOTE_REDIS_PORT'] = "test"
    import settings

def test_pcap_queue():
    """ Tests simulation of new pcap """
    file_watch.pcap_queue("/tmp")
    file_watch.pcap_queue("/dev/null")


def test_template_queue():
    """ Tests simulation of new/modified template """
    os.environ['HOSTNAME'] = "test"
    os.system('docker run -d alpine:latest /bin/sh -c "echo hello world;"')
    os.system('docker run --name core-template-queue1 -d alpine:latest /bin/sh -c "while true; do echo hello world; sleep 1; done"')
    os.system('docker run --name active-template-queue1 -d alpine:latest /bin/sh -c "while true; do echo hello world; sleep 1; done"')
    os.system('docker run --name passive-template-queue1 -d alpine:latest /bin/sh -c "while true; do echo hello world; sleep 1; done"')
    os.system('docker run --name visualization-template-queue1 -d alpine:latest /bin/sh -c "while true; do echo hello world; sleep 1; done"')
    file_watch.template_queue("/dev/null")
    file_watch.template_queue("/modes.template")
    file_watch.template_queue("/core.template")
    file_watch.template_queue("/collectors.template")
    file_watch.template_queue("/visualization.template")

    os.environ['HOSTNAME'] = subprocess.check_output('docker run --name core-template-queue2 -d alpine:latest /bin/sh -c "while true; do echo hello world; sleep 1; done"', shell=True)
    file_watch.template_queue("/core.template")
    os.environ['HOSTNAME'] = subprocess.check_output('docker run --name active-template-queue2 -d alpine:latest /bin/sh -c "while true; do echo hello world; sleep 1; done"', shell=True)
    file_watch.template_queue("/collectors.template")
    os.environ['HOSTNAME'] = subprocess.check_output('docker run --name passive-template-queue2 -d alpine:latest /bin/sh -c "while true; do echo hello world; sleep 1; done"', shell=True)
    file_watch.template_queue("/collectors.template")
    os.environ['HOSTNAME'] = subprocess.check_output('docker run --name visualization-template-queue2 -d alpine:latest /bin/sh -c "while true; do echo hello world; sleep 1; done"', shell=True)
    file_watch.template_queue("/visualization.template")
