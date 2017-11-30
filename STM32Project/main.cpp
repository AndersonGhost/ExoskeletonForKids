/*
This file is what runs in the STM32 board system.
*/
#include "mbed.h"
# include "hip.h"
# include "knee.h"

DigitalOut led1(LED1); // blink and debug
DigitalOut led2(LED2);
Serial pc(USBTX,USBRX,115200);

void periodic_function()
{
    static int counter = 0;
    counter++;
    if((counter%1000)==0) {
        led2=!led2;
    }
}

// main() runs in its own thread in the OS
int main()
{
    pc.printf("main\n\r");
    
    Ticker control_loop;
    control_loop.attach(&periodic_function, 0.001);
    bool stop = 0;
    TrajectoryGenerator generator;
    float hipAngle;
    while (true) {
        if (pc.readable()) {
            char c = pc.getc();
            pc.printf("User inserted: %c\n\r",c);
            led1 = !led1;
            stop = !stop;
            if (stop)
                generator.stopTrigger();
            else 
                generator.resumeTrigger();
        }
        hipAngle = generator.generateTrajectory();
    }
}