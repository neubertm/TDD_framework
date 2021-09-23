#include "PaperInterface.hpp"

using ::CPaperInterface;

class CPencil
{
	public: 

	CPencil(CPaperInterface &r_pPaper1, CPaperInterface &r_pPaper2);

	~CPencil();

	void eraseAll(void);

	void setPaper(int i_pPaperNumber);

	void writeString(char *p_pString, int i_pLength);

	bool eraseLastSpecificCharacter(char c_pCharacter);

	void eraseAllSameCharacters(char c_pCharacter);

	private:

	CPaperInterface &r_mPaper1;

	CPaperInterface &r_mPaper2;

	CPaperInterface *p_mCurrentPaper;

};
