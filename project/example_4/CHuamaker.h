#pragma once

class CPrinter;

class CHuamaker {

 private:

	// printer
	CPrinter *po_mPrinter;

 public:

	// constructor
	CHuamaker();

	// destruktor
	~CHuamaker();

	// make hua n times
	void makeHua(unsigned int uint_pCount);

	// set printer object
	void setPrinter(CPrinter *po_pPrinter);

};

