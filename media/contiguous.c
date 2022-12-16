#include <stdio.h>
#include <stdlib.h>

int main(){
    int mem_size, req, nof;
    printf("Enter the total memory size: ");
    scanf("%d", &mem_size);
    int *filled = (int*) malloc(mem_size*sizeof(int));
    for(int i=0;i<(sizeof(filled)/sizeof(int));i++){
        filled[i] = 0;
    }
    printf("Enter the required size: ");
    scanf("%d", &req);
    printf("Enter the number of memory locations already occupied between 1 and %d: ", mem_size);
    scanf("%d", &nof);
    printf("Enter the locations: ");
    for(int i=0;i<nof;i++){
        int temp;
        scanf("%d", &temp);
        filled[temp-1] = 1;
    }
    int pos = -1, flag=0;
    for(int i=0;i<mem_size;i++){
        flag = 0;
        if (filled[i] == 0){
            if((i+req) <= mem_size){
            for(int j=i;j<(i+req);j++){
                if (filled[j] == 1){
                    flag = 1;
                }
            }
            }
            else{
                pos = -1;
                break;
            }
            if (flag == 0){
                pos = i;
                break;
            }
            
        }
    }

    if (pos == -1){
        printf("No Memory available!!!");
    }
    else{
    printf("\nMemory allocated: %d", pos+1);
    for(int i=1;i<req;i++){
        printf("->%d",pos+i+1);
    }
    printf("\n");
    }
}