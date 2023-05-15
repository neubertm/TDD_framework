#ifndef CPrinter_H
#define CPrinter_H

//void foo(void);

class CPrinter {

 public:

	// constructor
	CPrinter()=default;

	// destruktor
	~CPrinter()=default;

	// print
	void out(const char *cs_pText);
};

#endif