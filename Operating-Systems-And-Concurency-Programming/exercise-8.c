/*MIT License
Copyright (c) 2020: 
Rafał Niebowziemii Stachowiak
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.*/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
int main(int argc,char** argv){
    if(argc==1){
        int fd[2];
        int fd2[2];
        pipe(fd);
        pipe(fd2);
        if(fork()==0){     
            dup2(fd[1],1);
            close(fd[1]);
            close(fd[0]);
            close(fd2[1]);
            close(fd2[0]);
            execlp("ls","ls", "-l", "/tmp",NULL);
        }    
        else{
            if(fork()==0){  
                dup2(fd[0],0);
                dup2(fd2[1],1);
                close(fd[1]);
                close(fd[0]);
                close(fd2[1]);
                close(fd2[0]);
                execlp("sort","sort" ,"-n" ,"-k", "5,5",NULL);
            }   
            else{
                dup2(fd2[0],0);
                close(fd2[1]);
                close(fd2[0]);
                close(fd[1]);
                close(fd[0]);
                execlp("tail","tail", "-5",NULL);
            }
        }
    return EXIT_SUCCESS;
}}
