#define switches (volatile short int *) 0x00020A0
#define Redleds (short int *) 0x0002090

#define hex0_1 (char *)(0x00002080)
#define hex2_3 (char *)(0x00002060)
#define hex4_5 (char *)(0x00002070)


int main()
{
	while (1)	{
		*Redleds = *switches;
		*hex0_1 = *switches ;
		*hex2_3 = *switches ;
		*hex4_5 = *switches ;
	}
	return 0 ;
}