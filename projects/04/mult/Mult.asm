// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

    @i
    M=0 // set i to 0
    @R2
    M=0 // set multipliacation result to 0

    // If R0 or R1 equals 0 end the program, result is 0
    @R0
    D=M
    @END
    D;JEQ
    @R1
    D=M
    @END
    D;JEQ

    // We need to check R0 and R1 signs for proper multipliacation in
    // case of negative numbers
    @CHECKRSIGNS
    0;JMP

(CHECKRSIGNS)
    // if R0 is negative change to positive
    @R0
    D=M
    @LOOP
    D;JGT
    @R0
    M=-M

    // if R0 and R1 is negative change R1 to positive too
    @R1
    D=M
    @LOOP
    D;JGT
    @R1
    M=-M

// Main loop where we and R1 to R2, R0 times
(LOOP)
    // Checking loop condition
    @i
    D=M
    @R0
    D=M-D
    @END
    D;JEQ

    @R1
    D=M
    @R2
    M=D+M // R2+=R1
    @i
    M=M+1 // i=i+1
    @LOOP
    0;JMP

(END)
    @END
    0;JMP




