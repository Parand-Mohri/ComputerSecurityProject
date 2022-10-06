#Assignment 1
####The goal of this assignment is to gain access to the secret message in a C-file. The program gets an input string from user, it's important to note that the length of such input has no limitation. Hence, a buffer overflow attack is possible. The file contains a method that prints the secret message, so if we can retrieve the memory address of such method and include it in our input string we can achieve our goal. For this, we must take into consideration the original length of input str to overwrite the pointer and add the address of the latter method. 
###Starting virtual machine
####The following assignment is carried on in a Linux environment, for this reason a virtual machine is needed to simulate Ubuntu and proceed to get the end result. First thing is to install gcc, the C compiler, and to share the files we are going to need. In the virtual machine settings we can make permanent folders to share between the host and the virtual env. 
sudo mount -t vboxsf assignment1 /home/ubuntu/Documents/shared
####,where assignment1 is the shared folder that contains the C-file to be exploited, and the path is a new directory we created on the VM. 

####Such attack is by default prevented, so for the sake of the assignment the ASLR was disabled with the following command: 
echo 0 | sudo tee /proc/sys/kernel/randomize_va_space
####Following, the assignment.c file was complied using the next command to disable the stack protector to enable the buffer overflow attack.
gcc -fno-stack-protector -z execstack -g assignment.c -o executable 
#### where -o executable is the result (the binary executable) of compiling assignment.c
###Getting the memory address
####Linux offers a debug mode, gdb, that by; we can see the code, add breakpoints and so on. 
gdb assignment -tui 
####In order to access the reliable memory address of the method introduced at the start, the code must first 'run'. Thus, a breakpoint was created at the main method, such that the program is already running but no alteratios are made yet. With the following command we can retrieve the address of the wanted method
info adress print_secret_message 
####and this was returned 
0x555555552db
###Buffer overflow attack 
####In another file, I used exploit.c from the first tutorial, the twixed input string will be declared: it was already explained at the begging, it will be 256 + 8 x's (the declared length for input str plus 8bits of the pointer ) plus the memory address we just retrieved. This file is also compiled with the following 
gcc exploit.c -o output 
####The next step is to run both files at the same time, such that the str declared in exploit is the input of assignment.c
./output | ./executable 
#### that returned the following, 
OLZLJYLATLZZHNLPZHNYLLHISLULZZLZ
#### so we retrieved the secret message! by accessing print_secret_message() with its corresponding memory address and calling it such that it printed the secret message! 







