#include "CPrinter.h"
#include <stdlib.h>
#include <cstring>
#include <stdio.h>


// print
void CPrinter::out(const char *cs_pText)
{
	sprintf(savedOutput+size,cs_pText);
	size += (unsigned int) std::strlen(cs_pText);
}

char* CPrinter::getOutput()
{
	return (char*)savedOutput;
}
