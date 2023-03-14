#include "CHuamaker.h"
#include "CPrinter.h"

// constructor
CHuamaker::CHuamaker(void)
  : po_mPrinter{nullptr}
{
}

// destructor
CHuamaker::~CHuamaker(void)
{
}

// make hua n times
void CHuamaker::makeHua(unsigned int uint_pCount)
{
	// we already have a printer
	if (nullptr != po_mPrinter)
	{
		// let's hua :)
		for (unsigned int i = 0; i < uint_pCount; i++)
		{
			// call printer
			po_mPrinter->out("hua ");
		}

		// call printer
		po_mPrinter->out("!!!");
	}
	// we don't have a printer
	else
	{
		// nothing to do, nobody can hear complains
	}
}

// set printer
void CHuamaker::setPrinter(CPrinter *po_pPrinter)
{
	//int i = 0;

	po_mPrinter = po_pPrinter;
	//i++;
}
