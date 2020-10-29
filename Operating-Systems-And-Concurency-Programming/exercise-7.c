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
#include <sys/time.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/stat.h>
#include <fcntl.h>

int main(int argc,char** argv){
    if(argc==1){
        return EXIT_FAILURE;
    }
    else{
        struct timeval tv1;
        struct timeval tv2;
        struct timeval res;
        gettimeofday(&tv1,NULL);
        if(fork()==0){            
            execvp(argv[1],(argv+1));
        }
        else{
            wait(NULL);
            gettimeofday(&tv2,0);
            timersub(&tv2,&tv1,&res);
            printf("%f",(res.tv_sec+(float)res.tv_usec / 1000000));
        }
    }
    return EXIT_SUCCESS;
}
