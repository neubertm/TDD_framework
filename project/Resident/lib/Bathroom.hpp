class CBathroom
{
	private:
	// private constructor and destructor - singleton class
	CBathroom();
	virtual ~CBathroom();
		  
    public:
    // singleton
	inline static CBathroom & instance()
	{
		static CBathroom o_slInstance;
		return o_slInstance;
	} 
	
	virtual void useShower(void);
			
	virtual void useWashBasin(void);
};