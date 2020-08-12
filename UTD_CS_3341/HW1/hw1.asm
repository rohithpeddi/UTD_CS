#Using MARS write a MIPS assembly language program to prompt the user to input two 32-bit integers X and Y (X and Y can be prompted separately or at the same time),
# get them from the user then store them in memory locations labeled X and Y respectively. 
#The program then loads X and Y from the main memory to registers, 
#calculates the sum of them (i.e. X + Y) and store the sum into a memory location labeled S. 
#The program then prints out the result (i.e. integer S) after printing the string "The sum of X and Y (X + Y) is 

			.data				#Indicates following data items are stored in the data segment
promptX: 		.asciiz	"\n Please input value for X "
promptY:		.asciiz 	"\n Please input value for Y "
promptSum:	.asciiz 	"\n The sum of X and Y (X + Y) is "
X:			.word 	0
Y:			.word	0	
S:			.word	0


			.text 				#Indicates items stored in the user text segment,[INSTRUCTIONS]
			.globl 	main			#Declare that main is global and can be referenced from other files
main:		
			la 		$a0, promptX 	#Load address of promptX into $a0
			li 		$v0, 4		#System call code for Print String
			syscall			
			li 		$v0, 5		#System call code for Read Integer
			syscall			
			move 	$t1, $v0		#Moving the user input of X  to register $t1
			sw		$t1, X		#Storing the input to word address X
						
			la 		$a0, promptY 	#Load address of promptX into $a0
			li 		$v0, 4		#System call code for Print String
			syscall			
			li 		$v0, 5		#System call code for Read Integer
			syscall			
			move 	$t2, $v0		#Moving the user input of Y to register $t2
			sw		$t2, Y		#Store the input to word address Y

			lw		$t3, X		#Loading X vakue from the stored word address
			lw 		$t4, Y		#Loading Y value from the stored word address
			add		$t5, $t3, $t4	#Summing up the values retrieved from X and Y addresses and storing in register $t5
			sw		$t5, S		#Storing the sum in word address S
			
			la 		$a0, promptSum 	#Load address of promptSum into $a0
			li 		$v0, 4		#System call code for Print String
			syscall
			
			lw		$a0, S		#Loads sum from the address S
			li		$v0, 1		#System call to print 
			syscall
			
			li 		$v0, 10		#Terminate program run 
			syscall				#Return control to system
			