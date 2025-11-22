1.先checksec以下

 <img width="811" height="363" alt="image" src="https://github.com/user-attachments/assets/6decbce1-2c37-4fd3-a79f-b0d2aeebec7c" />
 
pie没开，canany也没有\n

拖进ida里面从main函数开始进行静态分析，没有system和binsh，需要ret2libc

<img width="919" height="224" alt="image" src="https://github.com/user-attachments/assets/8560b386-f5c4-4dd4-b34d-2e73948f5b3e" />

<img width="1052" height="516" alt="image" src="https://github.com/user-attachments/assets/23314e16-aff3-40ec-81d4-e0421aca5e11" />

第一个函数是初始化，直接分析第二个函数，第一个read无溢出，但可以泄露栈上的地址，第二个read只能溢出16字节，刚好覆盖rbp和ret。

需要进行栈迁移
