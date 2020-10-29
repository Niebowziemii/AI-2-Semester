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
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
int main(int argc,char** argv){
    if(argc==3){
        int fd;
        int nf;
        mode_t mode = S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH;
        char buffer[65536];//64 KiB
        int read_byte;
        int write_byte;
        fd = open (argv [1], O_RDONLY);
        if (fd == -1) {
            printf("[error] Cannot open source file.");
            return EXIT_FAILURE;
        }
        nf = open(argv[2], O_WRONLY | O_CREAT | O_TRUNC, mode);
        if (nf == -1) {
            printf("[error] Cannot open destination file.");
            return EXIT_FAILURE;
        }
        memset(buffer,0,65536);
        while((read_byte=read(fd,buffer,65536))>0){
            write (nf, buffer, read_byte);
        }
        close(nf);
        close(fd);
        return EXIT_SUCCESS;
    }
    else{
        printf("Rafał Stachowiak\n use: ./filename <source_file> <destination_file>\n");
    }

}
