#include "CPrinter.h"
#include <stdio.h>

// constructor
CPrinter::CPrinter(void)
{
}

// destructor
CPrinter::~CPrinter(void)
{
}

// print text
void CPrinter::out(const char *cs_pText)
{
	printf("%s", cs_pText);
}

