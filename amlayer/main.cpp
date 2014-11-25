/* test3.c: tests deletion and scan. */
#include <cstdio>
#include <cstdlib>
#include <stdio.h>
#include <time.h>
#include <sys/time.h>
#include <stdlib.h>
#include <string.h>
#include "testam.h"
#include "amcppheader.h"
#include "data.h"
#include "am.h"
#include "pf.h"

#define MAXRECS	10000	/* max # of records to insert */
#define FNAME_LENGTH 80	/* file name size */
#define LINE_LENGTH 100 /* max length of line in stuff */

int space = 0;
int buf_access = 0;
int buf_miss = 0;
//int buf_hit;
int stringToInt(char *number) {
	int current, finalNumber, length, i;
	char character;
	current = 0;
	finalNumber = 0;
	i = 0;
	length = strlen(number);
	
	for (i=0; i<length; ++i) {
		character = number[i];
		current = character - '0';
		finalNumber = finalNumber*10 + current;
	}
	return finalNumber;
}

char* RELNAME1;

int main(int argc, char *argv[])
{
    if (argc > 1){
        RELNAME1 = argv[1];
    }
    else {
        return 0;
    }
int fd;	/* file descriptor for the index */
char fname[FNAME_LENGTH];	/* file name */
char buffer[LINE_LENGTH];
int recnum;	/* record number */
int sd;	/* scan descriptor */
int numrec;	/* # of records retrieved */
int testval;
char *pageBuf;
int pageNum;

struct timeval tv1, tv2;
FILE *fp = fopen(RELNAME1, "r");
int i=0, number=0;
int count = 0;

	PF_Init();

	AM_CreateIndex(RELNAME1,0,INT_TYPE,sizeof(int));

	sprintf(fname,"%s.0",RELNAME1);
	fd = PF_OpenFile(fname);
	
	if (fp) {
		gettimeofday(&tv1, NULL);
		while (fgets(buffer, LINE_LENGTH, fp)) {
			number = stringToInt(buffer);
			AM_InsertEntry(fd, INT_TYPE, sizeof(int), (char *)&number, i);
			i++;
			count ++;
		}
		gettimeofday(&tv2, NULL);
		printf("%lf\n", (tv2.tv_usec/1000.0) - (tv1.tv_usec/1000.0));
		//Buffer_hit, Buffer_miss
		printf("%d %d\n", buf_access - buf_miss, buf_miss);
	}

	printf("%d %d\n", level, nodes);

	double space_util = (count* sizeof(int))*100.0/(nodes* PF_PAGE_SIZE);
	//Space utlization
	printf("%lf\n", space_util);


	//printf("Root Page Num: %d  Leftmost Page Num: %d\n", AM_RootPageNum, AM_LeftPageNum);


	/* destroy everything */
	PF_CloseFile(fd);
	AM_DestroyIndex(RELNAME1,0);

}
