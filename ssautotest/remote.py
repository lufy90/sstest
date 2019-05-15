#!/bin/env python36
# remote.py
# libraries about remote host


import paramiko
from scp import SCPClient

def ssh(ruser, rhost, rpassword, port=22):
  ssh = paramiko.SSHClient()
  ssh.load_system_host_keys()
  ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

  ssh.connect(rhost, port, ruser, rpassword)
  return ssh


def scp(ruser, rhost, rpassword, port=22):
  sshc = ssh(ruser, rhost, rpassword, port=22)
  return SCPClient(sshc.get_transport())


def ex_rhost(ruser, rhost, rpassword, cmd, port=22):
  sshc = ssh(ruser, rhost, rpassword, port=22)
  return sshc.exec_command(cmd, get_pty=True)

