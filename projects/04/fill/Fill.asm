// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

    // keep track of whether last key was 0, it will allow us to not redraw screen in some occasions
    @lastkey
    M=0
    @currentkey
    M=0

(MAINLOOP)
    @KBD
    D=M
    @KEYZERO // we need that to change specific key number to -1 if it is other then 0
    D;JEQ
    D=-1

(KEYZERO)
    @currentkey
    M=D
    @lastkey
    D=D-M
    @MAINLOOP
    D;JEQ

    // Updating lastkey
    @currentkey
    D=M
    @lastkey
    M=D

    // Drawing screen
    @SCREEN
    D=A
    @pixel
    M=D
    @DRAWLOOP
    0;JMP

(DRAWLOOP)
    @24576 // How many times we need to loop over screen 16-bit chunks to cover it all: 256 * 512 / 16 (8192) + @SCREEN (16384)
    D=A
    @pixel
    D=D-M
    @MAINLOOP
    D;JEQ // check if full screen has been redrawn

    // Drawing 16-bits
    @currentkey
    D=M
    @pixel
    A=M
    M=D
    // @16
    // D=A
    @pixel // update pixel position
    M=M+1

    @DRAWLOOP
    0;JMP


    




