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
