checksec一下，没开pie和金丝雀保护。

拖进ida里面进行分析。查看字符串，只有system没有binsh。

<img width="1227" height="716" alt="image" src="https://github.com/user-attachments/assets/2819ffb0-8fdd-4498-9d4b-6df68604f0ab" />

输入一个整数，传入introduce函数，有强制类型转换，输入-1可以造成溢出。

在introduce函数中读取数据存到bss段，在main中read函数可以造成溢出，但是只能溢出16字节。

需要进行栈迁移。

进行ROP。

<img width="1519" height="883" alt="image" src="https://github.com/user-attachments/assets/18bbb74b-9b00-4253-9c93-651bc2d3dd7c" />

构造payload

payload =b'a'*0x8a0 + b'/bin/sh\x00' + p64(pop_rdi) + p64(pivot) + p64(ret) + p64(system_plt)

不知道为什么要加上0x8a0个a，好像只要超过bss段最后的地址都可以，我试过不加，但是打不通。

写入system函数的第一个参数实在bss段+0x8a0处，ret好像是为了栈对齐，目前还不知道为什么

构造第二个payload进行栈迁移，需要在rdi前面预留8个字节给rbp，rbp填什么都可以，刚好使用/bin/sh\x00
payload2 = b'a'*0xc + p64(pivot) + p64(leave_ret)




