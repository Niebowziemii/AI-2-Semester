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
    // character by character
    for(int i=file_size-2;i>-1;i--){
        printf("%c",buffer[i]);
    }
    //line by line
    
    for(int i=0,k=file_size-1;i<(file_size/2);i++,k--){
        char temp=buffer[k];
        buffer[k]=buffer[i];
        buffer[i]=temp;
    }
    int begin=0,len=0;
    for(int i=0;i<file_size+2;i++){
        if(i==file_size-1){
                
                char*line=(char*)calloc(1,(file_size-begin));
                memcpy(line,&buffer[begin],file_size-begin);
                printf("%s\n",line);
                continue;
            }
        else if (buffer[i]=='\n'){
            len = i-begin;
            char* line=(char*)calloc(1,len);
            memcpy(line,&buffer[begin],len);
            printf("%s\n",line);
            begin=i+1;
            free(line);
        }
    }

fclose(fd);
return EXIT_SUCCESS;
}
