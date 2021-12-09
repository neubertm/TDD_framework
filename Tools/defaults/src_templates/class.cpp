/*!****************************************************************************
 *  \brief      This file implements
 *              ... class %COMPONENT_NAME
 *
 *
 *  \file       %FILENAME.cpp
 *
 *  \author     Name, Surname, email@address.here
 *
 *  \date       %DATE
 *
 *  \copyright  Copyright (C) %YEAR FILL_ORGANIZATION_NAME. All rights reserved.
 *****************************************************************************/

// =============================================================================
// Own includes
// =============================================================================
#include "%HEADER_FILENAME"

// =============================================================================
// Dependency includes
// =============================================================================

// =============================================================================
// Using following classes on global level
// =============================================================================
using ::%CLASSNAME;


// =============================================================================
// %CLASSNAME class implementation
// =============================================================================

%CLASSNAME::%CLASSNAME(Uint32_t ui32_pNumber)
: ui32_mNumber(ui32_pNumber)
{
}

%CLASSNAME::~%CLASSNAME()
{
}

Uint32_t %CLASSNAME::getNumber(void) const
{
    return ui32_mNumber;
}
