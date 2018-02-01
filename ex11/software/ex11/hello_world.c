#define key0 (volatile char *) 0x2040
#define key1 (volatile char *) 0x2020
#define key2 (volatile char *) 0x2010
#define key3 (volatile char *) 0x2000

#define hex (char *) 0x2030

void main()
{

	while(1){

		while(!* key0 && * key1 && * key2 && * key3){
			 * hex = 0b11000000; // a LSB
		}

		while(* key0 && !* key1 && * key2 && * key3){
			 * hex = 0b11111001;
		}
		while(* key0 && * key1 && !* key2 && * key3){
			 * hex = 0b10100100;
		}

		while(* key0 && * key1 && * key2 && !* key3){
			 * hex = 0b10110000;
		}
		 * hex = 0b11111111;

	}

}
