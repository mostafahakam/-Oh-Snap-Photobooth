/*
 * "Hello World" example.
 *
 * This example prints 'Hello from Nios II' to the STDOUT stream. It runs on
 * the Nios II 'standard', 'full_featured', 'fast', and 'low_cost' example
 * designs. It runs with or without the MicroC/OS-II RTOS and requires a STDOUT
 * device in your system's hardware.
 * The memory footprint of this hosted application is ~69 kbytes by default
 * using the standard reference design.
 *
 * For a reduced footprint version of this template, and an explanation of how
 * to reduce the memory footprint for a given application, see the
 * "small_hello_world" template.
 *
 */

#include <stdio.h>
#include <sys/alt_alarm.h>
#include <unistd.h>
#include <sys/alt_timestamp.h>

int main()
{
  printf("Hello from Nios II & Mac!\n");
  int a[100][100];
  int b[100][100];
  int c[100][100];
  int sum, i, k, j;
  float start_time, end_time;

  for (i=0; i<100; i++){
	  for(k=0; k<100; k++){
		  a[i][k] = i;
		  b[i][k] = k;
	  }
  }
  alt_timestamp_start();
  start_time = alt_timestamp();
  printf("Start time : %d  \n", start_time);

  for (i=0; i<100; i++){
	  for(j=0; j<100; j++){
		  sum = 0;
		  for(k=0;k<100;k++){
			  sum = sum + a[i][k]*b[k][j];
		  }
		  c[i][j] = sum;
	  }

  }

  end_time = alt_timestamp();
  printf("time taken: %f clock ticks \n", end_time-start_time);
  printf("            %f seconds \n", (float)(end_time-start_time)/(float)alt_timestamp_freq());



  return 0;
}
