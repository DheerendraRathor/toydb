#include <stdio.h>
#include <am.h>
#include <pf.h>

AM_SCreateIndex(fileName, indexNo, attrType, attrLength)
char *fileName; // Name of the indexed file
int indexNo; // Number of index for the given file
char attrType; // 'c' for char, 'i' for int, 'f' for float
int attrLength; // 4 for 'i' or 'f', 1-255 for 'c'
{
	/* initialize PF layer */
	printf("Initializing\n");
	PF_Init();
	
	char *pageBuf; // buffer for holding  a page
	int pageNum; // page number of the root page (also the first page)
	int maxKeys; // Maximum keys that can be held on one internal page (has to be even)
	AM_LEAFHEADER head, *header;
	
	if ((attrType!='c') && (attrType!='f') && attrType!='i')) {
		AM_Errno = AME_INVALIDATTRTYPE;
		return(AME_INVALIDATTRTYPE);
	}
	
	if ((attrLength<1) || (attrLength>255)) {
		AM_Errno = AME_INVALIDATTRLENGTH;
		return(AME_INVALIDATTRLENGTH);
	}
	
	if (attrLength!=4) {
		if (attrType!='c') {
			AM_Errno = AME_INVALIDATTRLENGTH;
			return(AME_INVALIDATTRLENGTH);
		}
	}
	
	header = &head;
	
	/* Create a paged file for index */
	int errVal; // For holding last error value
	errVal = PF_CreateFile("sorted");
	AM_Check;
	
	int fd; // File Descriptor
	fd = PF_OpenFile("sorted");
	if (fd<0) {
		AM_Errno = AME_PF;
		return(AME_PF);
	}
	
	errVal = PF_AllocPage(fd, &pageNum, &pageBuf);
	AM_Check;
	
	header->pageType = 'l';
	header->nextLeafPage = AM_NULL_PAGE;
	header->recIdPtr = PF_PAGE_SIZE;
	header->keyPtr = AM_sl;
	header->freeListPtr = AM_NULL;
	header->numinfreeList = 0;
	header->attrLength = attrLength;
	header->numKeys = 0;
	
	maxKeys = (PF_PAGE_SIZE - AM_sint - AM_si)/(AM_si + attrLength);
	if (maxKeys%2!=0) header->maxKeys = maxKeys-1;
	else header->maxKeys = maxKeys;
	
	bcopy(header, pageBuf, AM_sl);
	
	errVal = PF_UnfixPage(fd, pageNum, TRUE);
	AM_Check;
	
	errVal = PF_CloseFile(fd);
	AM_Check;
	
	AM_RootPageNum = pageNum;
	return(AME_OK);
}
