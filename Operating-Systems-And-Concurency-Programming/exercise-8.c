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
