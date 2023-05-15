#pragma once

#include <string>

class CPrinter {

 public:

	// constructor
	explicit CPrinter()
	: savedOutput()
	{
	}

	// destruktor
	~CPrinter()
	{
	}

	// print
	void out(const char *cs_pText);

	const char *getOutput();

	private:
	
	std::string savedOutput;

    CPrinter(const CPrinter&);
    CPrinter& operator=(const CPrinter&);

};
