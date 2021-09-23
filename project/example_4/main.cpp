#include "CHuamaker.h"
#include "CPrinter.h"
#include <stdlib.h>



int main(int argc, char *argv[])
{
	CPrinter o_lPrinter;
	CHuamaker o_lHuamaker;

	// no parameters set
	if (argc < 2)
	{
		o_lPrinter.out("Zadej cislo jako parametr\n");
	}
	// parameter set, let's hua
	else
	{
		// set printer for huamaker
		o_lHuamaker.setPrinter(&o_lPrinter);
		
		// run huamaker with parameter
		o_lHuamaker.makeHua(atoi(argv[1]));
	}
}

