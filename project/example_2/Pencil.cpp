#include "Pencil.hpp"

using ::CPaperInterface;

CPencil::CPencil(CPaperInterface &r_pPaper1, CPaperInterface &r_pPaper2) : r_mPaper1(r_pPaper1), r_mPaper2(r_pPaper2), p_mCurrentPaper(&r_pPaper1)
{

}

CPencil::~CPencil()
{
	
}

void CPencil::eraseAll(void)
{
	p_mCurrentPaper->replacePaper();
}

void CPencil::setPaper(int i_pPaperNumber)
{
	if(i_pPaperNumber == 1)
	{
		p_mCurrentPaper =  &r_mPaper1;
	}
	else
	{
		p_mCurrentPaper = &r_mPaper2;
	}
}

void CPencil::writeString(char *ps_pString, int i_pLength)
{
	for (int i = 0; i < i_pLength; i++)
	{
		char c_lCharacter = ps_pString[i];
		
		p_mCurrentPaper->writeCharacter(c_lCharacter);
	}
}

bool CPencil::eraseLastSpecificCharacter(char c_pCharacter)
{
	bool b_lSuccess = false;
	
	int i_lIndex = 0;
	
	i_lIndex = p_mCurrentPaper->getLastIndexOfCharacter(c_pCharacter);
	
	if (i_lIndex > 0)
	{
		p_mCurrentPaper->eraseCharacterOnIndex(i_lIndex);
		
		b_lSuccess = true;
	}
	else
	{
		b_lSuccess = false;
	}
	
	return b_lSuccess;
	
}

void CPencil::eraseAllSameCharacters(char c_pCharacter)
{
	int i_lCount = 0;
	
	p_mCurrentPaper->getCountOfCharacter(c_pCharacter, i_lCount);
	
	for (int i = 0; i < i_lCount; i++)
	{
		int i_lIndex = p_mCurrentPaper->getLastIndexOfCharacter(c_pCharacter);
		
		p_mCurrentPaper->eraseCharacterOnIndex(i_lIndex);
	}
}
