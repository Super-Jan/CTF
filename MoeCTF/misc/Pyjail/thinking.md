使用nc连接题目

Linux 遵循“一切皆文件”的设计理念，将系统资源（硬件、进程信息等）抽象为文件进行访问。而在这其中有：

/proc 是一个特殊的虚拟文件系统，它动态提供运行中进程的信息。

/proc/self 是一个符号链接，总是指向当前访问它的进程自身的信息目录。

/proc/self/environ 这个“文件”则包含了当前进程的所有环境变量。

/proc/self/environ 详解（渗透测试核心知识点）

一、核心定义

/proc/self/environ 是 Linux/Unix 系统中 proc 文件系统 的特殊文件，作用是：

实时存储 当前进程 的环境变量（如 PATH、USER、HOME、LD_LIBRARY_PATH 等）

self 是符号链接，指向当前访问该文件的进程 PID（无需手动指定进程号）

<img width="2315" height="336" alt="image" src="https://github.com/user-attachments/assets/b20e4a4e-38a4-4546-852f-158fa2064cb8" />
