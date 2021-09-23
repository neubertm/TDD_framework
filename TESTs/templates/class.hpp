/*!****************************************************************************
 *  \brief      This header file contains definition of
 *              ... class
 *
 *  \file       %%FILENAME.hpp
 *
 *  \author     XYz, X Yz, X.Yz@siemens.com
 *
 *  \date       %DATE
 *
 *  \copyright  Copyright (C) 2019 Siemens AG. All rights reserved.
 *****************************************************************************/

#ifndef %FILENAME_hpp_INCLUDED
#define %FILENAME_hpp_INCLUDED

// N2-1 Type definitions shall be used instead of the basic numerical types char, int, float, double etc.
#include "define.h"

// =============================================================================
// Required includes
// =============================================================================


class %CLASSNAME
{
private:
	// no instance copy
	%CLASSNAME(const %CLASSNAME &other);
	%CLASSNAME &operator=(const %CLASSNAME &other);
	
public:
	// <summary>
	//   Initializes new instance.
	// </summary>
	// <param name="ui32_pNumber">
	//   This parameter of type <c>ui32_t</c> defines the number which will be returned by "getNumber" function.
	// </param>
	explicit %CLASSNAME(Uint32_t ui32_pNumber);
	virtual ~%CLASSNAME();
	
public:
	
	// <summary>
	//   Gets original parameter value from constructor.
	// </summary>
	// <returns>
	//   <c>Uint32_t</c> value.
	// </returns>
	virtual Uint32_t getNumber(void) const;
	
private:

	// <summary>
	//   Stored number.
	// </summary>
	Uint32_t ui32_mNumber;
};


#endif // Emitter%PACKAGENAME_%FILENAME_hpp_INCLUDED
