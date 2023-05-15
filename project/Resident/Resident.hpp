#include "lib/Bathroom.hpp"

class CResident
{
	public:
	
	CResident();
	
	~CResident();
	
	void washHands(void);
	
	void takeAShower(void);
	
	private:
	
	CBathroom &ro_mBathroom;
	
};