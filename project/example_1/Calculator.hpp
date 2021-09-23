class CCalculator
{
	public:

	CCalculator();

	~CCalculator();

	int getResult(void);

	int multiply(int a, int b);

	void divide(float &a, float &b, float &p_result);

	float divide(const float a, const float b);

	private:

	int result;

};
