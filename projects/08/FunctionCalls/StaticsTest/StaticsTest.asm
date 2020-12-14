	@256
	D=A
	@SP
	M=D // Set SP (RAM[0]) to 256
	@return_address-0
	D=A
	@SP
	A=M
	M=D // save return-address on the stack
	@SP
	M=M+1 // update the stack
	@LCL
	D=M
	@SP
	A=M
	M=D // save LCL of the calling function
	@SP
	M=M+1
	@ARG
	D=M
	@SP
	A=M
	M=D // save ARG of the calling function
	@SP
	M=M+1
	@THIS
	D=M
	@SP
	A=M
	M=D // save THIS of the calling function
	@SP
	M=M+1
	@THAT
	D=M
	@SP
	A=M
	M=D // save THAT of the calling function
	@SP
	M=M+1
	@5
	D=A
	@SP
	D=M-D
	@ARG
	M=D // Reposition ARG (SP-num_args-5)
	@SP
	D=M
	@LCL
	M=D // Reposition LCL (LCL = SP)
	@Sys.init
	0;JMP // Transfer control (goto f)
(return_address-0) // Declare label for the return-address
(Sys.init) // HANDLING FUNCTION
	@SP
	D=M
	A=D
	M=0
	@SP
	M=D
	@6
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1
	@8
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1
	@return_address-1
	D=A
	@SP
	A=M
	M=D // save return-address on the stack
	@SP
	M=M+1 // update the stack
	@LCL
	D=M
	@SP
	A=M
	M=D // save LCL of the calling function
	@SP
	M=M+1
	@ARG
	D=M
	@SP
	A=M
	M=D // save ARG of the calling function
	@SP
	M=M+1
	@THIS
	D=M
	@SP
	A=M
	M=D // save THIS of the calling function
	@SP
	M=M+1
	@THAT
	D=M
	@SP
	A=M
	M=D // save THAT of the calling function
	@SP
	M=M+1
	@7
	D=A
	@SP
	D=M-D
	@ARG
	M=D // Reposition ARG (SP-num_args-5)
	@SP
	D=M
	@LCL
	M=D // Reposition LCL (LCL = SP)
	@Class1.set
	0;JMP // Transfer control (goto f)
(return_address-1) // Declare label for the return-address
	@R0
	D=A
	@R5
	A=A+D
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M-1
	@SP
	A=M
	D=M
	@SP
	A=M+1
	A=M
	M=D
	@23
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1
	@15
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1
	@return_address-2
	D=A
	@SP
	A=M
	M=D // save return-address on the stack
	@SP
	M=M+1 // update the stack
	@LCL
	D=M
	@SP
	A=M
	M=D // save LCL of the calling function
	@SP
	M=M+1
	@ARG
	D=M
	@SP
	A=M
	M=D // save ARG of the calling function
	@SP
	M=M+1
	@THIS
	D=M
	@SP
	A=M
	M=D // save THIS of the calling function
	@SP
	M=M+1
	@THAT
	D=M
	@SP
	A=M
	M=D // save THAT of the calling function
	@SP
	M=M+1
	@7
	D=A
	@SP
	D=M-D
	@ARG
	M=D // Reposition ARG (SP-num_args-5)
	@SP
	D=M
	@LCL
	M=D // Reposition LCL (LCL = SP)
	@Class2.set
	0;JMP // Transfer control (goto f)
(return_address-2) // Declare label for the return-address
	@R0
	D=A
	@R5
	A=A+D
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M-1
	@SP
	A=M
	D=M
	@SP
	A=M+1
	A=M
	M=D
	@return_address-3
	D=A
	@SP
	A=M
	M=D // save return-address on the stack
	@SP
	M=M+1 // update the stack
	@LCL
	D=M
	@SP
	A=M
	M=D // save LCL of the calling function
	@SP
	M=M+1
	@ARG
	D=M
	@SP
	A=M
	M=D // save ARG of the calling function
	@SP
	M=M+1
	@THIS
	D=M
	@SP
	A=M
	M=D // save THIS of the calling function
	@SP
	M=M+1
	@THAT
	D=M
	@SP
	A=M
	M=D // save THAT of the calling function
	@SP
	M=M+1
	@5
	D=A
	@SP
	D=M-D
	@ARG
	M=D // Reposition ARG (SP-num_args-5)
	@SP
	D=M
	@LCL
	M=D // Reposition LCL (LCL = SP)
	@Class1.get
	0;JMP // Transfer control (goto f)
(return_address-3) // Declare label for the return-address
	@return_address-4
	D=A
	@SP
	A=M
	M=D // save return-address on the stack
	@SP
	M=M+1 // update the stack
	@LCL
	D=M
	@SP
	A=M
	M=D // save LCL of the calling function
	@SP
	M=M+1
	@ARG
	D=M
	@SP
	A=M
	M=D // save ARG of the calling function
	@SP
	M=M+1
	@THIS
	D=M
	@SP
	A=M
	M=D // save THIS of the calling function
	@SP
	M=M+1
	@THAT
	D=M
	@SP
	A=M
	M=D // save THAT of the calling function
	@SP
	M=M+1
	@5
	D=A
	@SP
	D=M-D
	@ARG
	M=D // Reposition ARG (SP-num_args-5)
	@SP
	D=M
	@LCL
	M=D // Reposition LCL (LCL = SP)
	@Class2.get
	0;JMP // Transfer control (goto f)
(return_address-4) // Declare label for the return-address
(Sys.init$WHILE)
	@Sys.init$WHILE
	0;JMP
(Class2.set) // HANDLING FUNCTION
	@SP
	D=M
	A=D
	M=0
	@SP
	M=D
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
	M=M-1
	A=M
	D=M
	@Class2.0
	M=D
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
	M=M-1
	A=M
	D=M
	@Class2.1
	M=D
	@0
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1
	@LCL
	D=M
	@R8 // FRAME temp var storing LCL address
	M=D
	@5
	A=D-A // LCL - 5
	D=M
	@R9
	M=D // Return address *(FRAME - 5)
	@SP
	M=M-1
	A=M
	D=M
	@ARG
	A=M
	M=D // *ARG = pop()
	@ARG
	D=M
	@SP
	M=D+1 // Restore SP of the caller
	@R8
	M=M-1 // FRAME - 1
	A=M
	D=M
	@THAT
	M=D // Restore THAT of the caller *(FRAME - 1)
	@R8
	M=M-1 // FRAME - 2
	A=M
	D=M
	@THIS
	M=D // Restore THIS of the caller *(FRAME - 2)
	@R8
	M=M-1 // FRAME - 3
	A=M
	D=M
	@ARG
	M=D // Restore THIS of the caller *(FRAME - 3)
	@R8
	M=M-1 // FRAME - 4
	A=M
	D=M
	@LCL
	M=D // Restore THIS of the caller *(FRAME - 4)
	@R9
	A=M
	0;JMP // Goto return-address (in the callers code)
(Class2.get) // HANDLING FUNCTION
	@SP
	D=M
	A=D
	M=0
	@SP
	M=D
	@Class2.0
	D=M
	@SP
	A=M
	M=D
	@SP
	M=M+1
	@Class2.1
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
	@R8 // FRAME temp var storing LCL address
	M=D
	@5
	A=D-A // LCL - 5
	D=M
	@R9
	M=D // Return address *(FRAME - 5)
	@SP
	M=M-1
	A=M
	D=M
	@ARG
	A=M
	M=D // *ARG = pop()
	@ARG
	D=M
	@SP
	M=D+1 // Restore SP of the caller
	@R8
	M=M-1 // FRAME - 1
	A=M
	D=M
	@THAT
	M=D // Restore THAT of the caller *(FRAME - 1)
	@R8
	M=M-1 // FRAME - 2
	A=M
	D=M
	@THIS
	M=D // Restore THIS of the caller *(FRAME - 2)
	@R8
	M=M-1 // FRAME - 3
	A=M
	D=M
	@ARG
	M=D // Restore THIS of the caller *(FRAME - 3)
	@R8
	M=M-1 // FRAME - 4
	A=M
	D=M
	@LCL
	M=D // Restore THIS of the caller *(FRAME - 4)
	@R9
	A=M
	0;JMP // Goto return-address (in the callers code)
(Class1.set) // HANDLING FUNCTION
	@SP
	D=M
	A=D
	M=0
	@SP
	M=D
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
	M=M-1
	A=M
	D=M
	@Class1.0
	M=D
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
	M=M-1
	A=M
	D=M
	@Class1.1
	M=D
	@0
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1
	@LCL
	D=M
	@R8 // FRAME temp var storing LCL address
	M=D
	@5
	A=D-A // LCL - 5
	D=M
	@R9
	M=D // Return address *(FRAME - 5)
	@SP
	M=M-1
	A=M
	D=M
	@ARG
	A=M
	M=D // *ARG = pop()
	@ARG
	D=M
	@SP
	M=D+1 // Restore SP of the caller
	@R8
	M=M-1 // FRAME - 1
	A=M
	D=M
	@THAT
	M=D // Restore THAT of the caller *(FRAME - 1)
	@R8
	M=M-1 // FRAME - 2
	A=M
	D=M
	@THIS
	M=D // Restore THIS of the caller *(FRAME - 2)
	@R8
	M=M-1 // FRAME - 3
	A=M
	D=M
	@ARG
	M=D // Restore THIS of the caller *(FRAME - 3)
	@R8
	M=M-1 // FRAME - 4
	A=M
	D=M
	@LCL
	M=D // Restore THIS of the caller *(FRAME - 4)
	@R9
	A=M
	0;JMP // Goto return-address (in the callers code)
(Class1.get) // HANDLING FUNCTION
	@SP
	D=M
	A=D
	M=0
	@SP
	M=D
	@Class1.0
	D=M
	@SP
	A=M
	M=D
	@SP
	M=M+1
	@Class1.1
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
	@R8 // FRAME temp var storing LCL address
	M=D
	@5
	A=D-A // LCL - 5
	D=M
	@R9
	M=D // Return address *(FRAME - 5)
	@SP
	M=M-1
	A=M
	D=M
	@ARG
	A=M
	M=D // *ARG = pop()
	@ARG
	D=M
	@SP
	M=D+1 // Restore SP of the caller
	@R8
	M=M-1 // FRAME - 1
	A=M
	D=M
	@THAT
	M=D // Restore THAT of the caller *(FRAME - 1)
	@R8
	M=M-1 // FRAME - 2
	A=M
	D=M
	@THIS
	M=D // Restore THIS of the caller *(FRAME - 2)
	@R8
	M=M-1 // FRAME - 3
	A=M
	D=M
	@ARG
	M=D // Restore THIS of the caller *(FRAME - 3)
	@R8
	M=M-1 // FRAME - 4
	A=M
	D=M
	@LCL
	M=D // Restore THIS of the caller *(FRAME - 4)
	@R9
	A=M
	0;JMP // Goto return-address (in the callers code)
(END)
	@END
	0;JMP
