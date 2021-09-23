class CPaperInterface
{
	public:
	
	CPaperInterface()
	{
		
	};
	
	~CPaperInterface()
	{
		
	};
	
	virtual void replacePaper(void) = 0;
			
	virtual void writeCharacter(char c_pCharacter) = 0;
	
	virtual int getLastIndexOfCharacter(char c_pCharacter) = 0;
	
	virtual void eraseCharacterOnIndex(int i_pIndex) = 0;
	
	virtual void getCountOfCharacter(char &rc_pCharacter, int &ri_pCount) = 0;
	
};