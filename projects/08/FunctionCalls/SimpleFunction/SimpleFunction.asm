(SimpleFunction.test) // HANDLING FUNCTION
	@SP
	D=M
	A=D
	M=0
	D=D+1
	A=D
	M=0
	@SP
	M=D
	@R0
	D=A
	@LCL
	A=M+D
	D=M
	@SP
	A=M
	M=D
	@SP
	M=M+1
	@R1
	D=A
	@LCL
	A=M+D
	D=M
	@SP
	A=M
	M=D
	@SP
	M=M+1
	@SP
	A=M-1
	D=M
	A=A-1
	M=M+D
	@SP
	M=M-1
	@SP
	A=M-1
	M=!M
	@R0
	D=A
	@ARG
	A=M+D
	D=M
	@SP
	A=M
	M=D
	@SP
	M=M+1
	@SP
	A=M-1
	D=M
	A=A-1
	M=M+D
	@SP
	M=M-1
	@R1
	D=A
	@ARG
	A=M+D
	D=M
	@SP
	A=M
	M=D
	@SP
	M=M+1
	@SP
	A=M-1
	D=M
	A=A-1
	M=M-D
	@SP
	M=M-1
	@LCL
	D=M
	@5 // FRAME temp var storing LCL address
	M=D
	@R5
	A=D-A // LCL - 5
	D=M
	@6
	M=D // Return address *(LCL - 5)
	@SP
	A=M-1
	D=M
	@ARG
	A=M
	M=D // *ARG = pop()
	@ARG
	D=M
	@SP
	M=D+1 // Restore SP of the caller
	@5
	M=M-1 // FRAME - 1
	A=M
	D=M
	@THAT
	M=D // Restore THAT of the caller *(FRAME - 1)
	@5
	M=M-1 // FRAME - 2
	A=M
	D=M
	@THIS
	M=D // Restore THIS of the caller *(FRAME - 2)
	@5
	M=M-1 // FRAME - 3
	A=M
	D=M
	@ARG
	M=D // Restore THIS of the caller *(FRAME - 3)
	@5
	M=M-1 // FRAME - 4
	A=M
	D=M
	@LCL
	M=D // Restore THIS of the caller *(FRAME - 4)
	@6
	A=M
	0;JMP // Goto return-address (in the callers code)
(END)
	@END
	0;JMP
