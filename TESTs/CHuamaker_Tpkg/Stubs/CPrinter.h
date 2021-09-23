#pragma once

class CPrinter {

 public:

	// constructor
	explicit CPrinter()
	{
		size = 0;
		savedOutput[0] = 0;
	}

	// destruktor
	~CPrinter()
	{
	}

	// print
	void out(const char *cs_pText);

	char* getOutput();

	//this is part of autogenerate from  CPPUTEST_FRAMEWORK
	private:
	char savedOutput[1000];
	unsigned int size;

    CPrinter(const CPrinter&);
    CPrinter& operator=(const CPrinter&);

};
