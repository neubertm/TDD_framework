#include "CPrinter.h"


// print
void CPrinter::out(const char *cs_pText)
{
	savedOutput += cs_pText;
}

const char *CPrinter::getOutput()
{
	return savedOutput.c_str();
}
