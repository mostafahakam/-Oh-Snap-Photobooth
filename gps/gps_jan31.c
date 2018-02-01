#include <stdio.h>
#include <system.h>
#include <string.h>
#include <sys/alt_alarm.h>
#include <unistd.h>
#include <sys/alt_timestamp.h>
#include <string.h>
#define UART (volatile char *) 0x0002000
#define HEX0 (volatile char *) 0x00011040
#define LEDs (volatile char *) 0x00011060
#define SWITCHES (volatile char *) 0x0011050
#define PUSHBUTTON (volatile char *) 0x00110C0
#define HEX1 (volatile char *) 0x000110B0
#define HEX2 (volatile char *) 0x000110A0
#define HEX3 (volatile char *) 0x00011090
#define HEX4 (volatile char *) 0x00011080
#define HEX5 (volatile char *) 0x00011070


struct gps_coordinates {
	char message id[7];
	double utc_time[11];
	double latitude;
	char ns_ind[2];
	double longitude;
	char ew_ind[2];
	int gps_fix;
	int no_sat;
} gps;

int main() {
	printf("Hello!\n");
//	if(erase_log())
//		printf("cleared logs\n");
	while(1) {
		int check = *SWITCHES;
		if(check % 2 == 0) {
			if(*PUSHBUTTON) {
				printf("\n\nRefreshing values\n\n");
				int fix = get_gps();
				if(fix)
					printf("We have signal!\n");
				else
					printf("We don't have signal.\n");
				usleep(1000000);
			} else
				continue;
		} else {
			if(start_log()){
				printf("\n\nLogging started.\n");
				while(1) {
					if(*PUSHBUTTON) {
						printf("Snapshot taken. '%d'\n", snapshot_log());
						usleep(1000000);
						check = *SWITCHES;
						if(check % 4 == 0){
							dump_log();
							return 0;
						}

					}
				}
			} else
				printf("Logging failed\n");
		}
	}
	return 0;
}


struct gps get_gps() {
	const char * ID = "$GPGGA";
	FILE* fp;
	char incoming;
	int have_link = 0;
	char message[128];
	volatile char message_id[7];
	volatile char utc_time[11];
	volatile char ns_ind[2];
	volatile char ew_ind[2];
	volatile char latitude[10];
	volatile char longitude[11];
	volatile char gps_fix[2];
	volatile char no_sat[3];
	volatile int i = 0;
	volatile int j = 0;
	int check_type = 1;
	int hash;
	fp = fopen("/dev/uart_0", "r+");
	if(fp == NULL)
		printf("RS232 error. \n");
	else {
		while(check_type){
			while(incoming != '$') {
				incoming = getc(fp);
			}
			i=0;
			while(incoming != '\r') {
				*(message+i) = incoming;
				incoming = getc(fp);
				i++;
			}
			hash = strncmp(message, ID, 6);
//			printf("check = '%d'\n", hash);
/*			for(i=0; i<72; i++) {
				printf("%c", *(message+i));
			}
			printf("\n"); */
			if(hash == 0) {
				check_type = 0;
			}
		}
		i=0;
		j=0;
		while(message[j] != ',') {
			*(message_id+i) = *(message+j);
			i++;
			j++;
		}
		*(message_id+i) = '\0';
		i=0;
		j++;
		while(message[j] != ',') {
			*(utc_time+i) = *(message+j);
			i++;
			j++;
		}
		*(utc_time+i) = '\0';
		i=0;
		j++;
		while(message[j] != ',') {
			*(latitude+i) = *(message+j);
			i++;
			j++;
		}
		*(latitude+i) = '\0';
		i=0;
		j++;
		while(message[j] != ',') {
			*(ns_ind+i) = *(message+j);
			i++;
			j++;
		}
		*(ns_ind+i) = '\0';
		i=0;
		j++;
		while(message[j] != ',') {
			*(longitude+i) = *(message+j);
			i++;
			j++;
		}
		*(longitude+i) = '\0';
		i=0;
		j++;
		while(message[j] != ',') {
			*(ew_ind+i) = *(message+j);
			i++;
			j++;
		}
		*(ew_ind+i) = '\0';
		i=0;
		j++;
		while(message[j] != ',') {
			*(gps_fix+i) = *(message+j);
			i++;
			j++;
		}
		*(gps_fix+i) = '\0';
		if(gps_fix[0] == '1' || gps_fix[0] == '2')
			have_link = 1;
		else
			have_link = 0;

		i=0;
		j++;
		while(message[j] != ',') {
			*(no_sat+i) = *(message+j);
			i++;
			j++;
		}
		*(no_sat+i) = '\0';
		*LEDs = atoi(no_sat);

		printf("message id = '%s'\n", message_id);
		printf("utc time = '%s'\n", utc_time);
		printf("latitude = '%s'\n", latitude);
		printf("n/s indicator = '%s'\n", ns_ind);
		printf("longitude = '%s'\n", longitude);
		printf("e/w indicator = '%s'\n", ew_ind);
		printf("gps link = '%s'\n", gps_fix);
		printf("# of satelites = '%s'\n", no_sat);

		struct gps;
		
		gps->message_id = message_id;
		gps->utc_time = atof(utc_time);
		gps->latitude = atof(latitude);
		gps->ns_ind = ns_ind;
		gps->longitude = atof(longitude);
		gps->ew_ind = ew_ind;
		gps->gps_fix = atoi(gps_fix);
		gps->no_sat = atoi(no_sat);
		

	}
	fclose(fp);
	return gps;
}

int erase_log() {
	const char * REPLY = "$PMTK001,184,3*3D";
	const char * ERASE = "$PMTK184,1*22\r\n";
	FILE* fp;
	int check_type = 1;
	char incoming;
	char message[20];
	int i=0;
	int hash = 2;
	fp = fopen("/dev/uart_0", "r+");
		if(fp == NULL)
			printf("RS232 error. \n");
		else {
			fwrite(ERASE, strlen(ERASE), 1, fp);

			while(check_type){
						while(incoming != '$') {
							incoming = getc(fp);
						}
						i=0;
						while(incoming != '\r') {
							*(message+i) = incoming;
							incoming = getc(fp);
							i++;
						}
						*(message+i) = '\0';
						hash = strncmp(message, REPLY, 17);
//						printf("'%s' '%s' check = '%d'\n", message, REPLY, hash);
						if(hash == 0) {
							check_type = 0;
						}
			}
		}

	if(!fclose(fp))
		return 1;
	else
		return 0;
}

int start_log() {
	const char * REPLY = "$PMTK001,185,3*3C";
	const char * START = "$PMTK185,0*22\r\n";
	FILE* fp;
	int check_type = 1;
	char incoming;
	char message[20];
	int i=0;
	int checkcount = 0;
	int hash = 2;
	fp = fopen("/dev/uart_0", "r+");
		if(fp == NULL)
			printf("RS232 error. \n");
		else {
			fwrite(START, strlen(START), 1, fp);

			while(check_type && checkcount <100){
						while(incoming != '$') {
							incoming = getc(fp);
						}
						i=0;
						while(incoming != '\r') {
							*(message+i) = incoming;
							incoming = getc(fp);
							i++;
						}
						*(message+i) = '\0';
						hash = strncmp(message, REPLY, 17);
//						printf("'%s' '%s' check = '%d'\n", message, REPLY, hash);
						if(hash == 0) {
							check_type = 0;
						}
			}
		}

	if(!fclose(fp))
		return 1;
	else
		return 0;
}

int snapshot_log() {
	const char * REPLY = "$PMTK001,186,3*3F";
	const char * SNAP = "$PMTK186,1*20\r\n";
	FILE* fp;
	int check_type = 1;
	char incoming;
	char message[20];
	int i=0;
	int hash = 2;
	fp = fopen("/dev/uart_0", "r+");
		if(fp == NULL)
			printf("RS232 error. \n");
		else {
			fwrite(SNAP, strlen(SNAP), 1, fp);

			while(check_type){
						while(incoming != '$') {
							incoming = getc(fp);
						}
						i=0;
						while(incoming != '\r') {
							*(message+i) = incoming;
							incoming = getc(fp);
							i++;
						}
						*(message+i) = '\0';
						hash = strncmp(message, REPLY, 17);
//						printf("'%s' '%s' check = '%d'\n", message, REPLY, hash);
						if(hash == 0) {
							check_type = 0;
						}
			}
		}

	if(!fclose(fp))
		return 1;
	else
		return 0;
}

int dump_log() {
	const char * REPLY = "$PMTK001,622,3*36";
	const char * DUMP = "$PMTK622,1*29\r\n";
	FILE* fp;
	int check_type = 1;
	char incoming;
	char message[20];
	char *dump;
	int i=0;
	int hash = 2;
	fp = fopen("/dev/uart_0", "r+");
		if(fp == NULL)
			printf("RS232 error. \n");
		else {
			fwrite(DUMP, strlen(DUMP), 1, fp);

			while(check_type){
						int j=0;
						while(incoming != '$') {
							incoming = getc(fp);
						}
						i=0;
						while(incoming != '\r') {
							*(message+i) = incoming;
							*(dump+j) = incoming;
							incoming = getc(fp);
							i++;
							j++;
						}
						*(message+i) = '\0';
						*(dump+i) = '\0';
						hash = strncmp(message, REPLY, 17);
//						printf("'%s' '%s' check = '%d'\n", message, REPLY, hash);
						if(hash == 0) {
							check_type = 0;
						}
			}
			printf("\n\n%s\n\n", dump);
		}

	if(!fclose(fp))
		return 1;
	else
		return 0;
}
