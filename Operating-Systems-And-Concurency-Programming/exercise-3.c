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
#include <string.h>

int main(int argc,char** argv){
    
    off_t file_size;
    char*buffer;
    struct stat buf;
    FILE* fd;

    fd = fopen(argv[1],"rb");
    if (fd==NULL){
        fprintf(stderr,"File is has not been opened.");
        return EXIT_FAILURE;
    }

    if((fstat(fileno(fd),&buf)!=0)||(!S_ISREG(buf.st_mode))) {
        fprintf(stderr,"This program works only with regular files.");
        return EXIT_FAILURE;
    }

    file_size=buf.st_size;
    buffer = (char*)calloc(file_size,sizeof(char));
    if(buffer==NULL){
        fprintf(stderr,"Problem in allocating memory for the file.");
        return EXIT_FAILURE;
    }
    fread(buffer,sizeof(char),file_size,fd);
    int countnl=0,count=0;
    for(int i =0;i<file_size;i++){
        count++;
        if(buffer[i]=='\n'){
            countnl++;
        }
    }
    printf("character num:\t %d\nnew line num:\t %d\n",count-1,countnl);
    fclose(fd);
    return EXIT_SUCCESS;
}
