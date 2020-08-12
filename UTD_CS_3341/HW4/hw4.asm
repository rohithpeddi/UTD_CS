# Prompts the user for a zip code (as a 5-digits unsigned integer, or 0) with the string "Give me your zip code (0 to stop): ". No error checking is necessary, assuming that the user will give correct numbers..
# If the input is 0 stops,  Otherwise, display the leading string
# "The sum of all digits in your zip code is", calculate the sum of all digits by calling two functions (see below) one at a time and then display the result with the leading string "ITERATIVE:"  for the iterative version, and "RECURSIVE:"  for the recursive version of the function.				
									
			.data				#Indicates following data items are stored in the data segment
promptX: 		.asciiz	"\n Give me your zip code (0 to stop): "
promptSum:	.asciiz 	"\n The sum of all digits in your zip code is: "
promptIt:		.asciiz	"\n ITERATIVE "
promptRec:	.asciiz	"\n RECURSIVE "
list:  			.word	100			# Space to store the words of integers

.text 				#Indicates items stored in the user text segment,[INSTRUCTIONS]
			.globl 	main			#Declare that main is global and can be referenced from other files
main:		
			la 		$a0, promptX 		#Load address of promptX into $a0
			li 		$v0, 4			#System call code for Print String
			syscall			
			li 		$v0, 5			#System call code for Read Integer
			syscall			
			move 	$s0, $v0			#Moving the user input  to register $s0
			beq		$s0, 0, exit		#Exit program execution if user inputs 0
						
			add		$a0, $s0, $zero	#Passing the user input as argument
			jal		ITERATIVE
			
			add		$a0, $s0, $zero	#Passing the user input as argument
			jal		RECURSIVE
			add		$a0, $v0, $zero
			jal		PRINTSUMREC
					
exit:			li 		$v0, 10		#Terminate program run 
			syscall				#Return control to system


# -------------------------------------------------------------  FUNCTION FOR ITERATIVE CALCULATION -------------------------------------------------------

ITERATIVE:	addi 		$sp, $sp, -8
			sw 		$s0, 0($sp)
			sw		$ra, 4($sp)
			
			add		$t1, $a0, $zero 	#Move user input acquired from argument to temporary register $t1
itSum:		sle		$t0, $t1, 0		#If user input is equal to zero then exit 
			beq		$t0, 1, print		#Based on set less than or equal condition we can branch to printsum 
			div		$t1, $t1, 10		#Divide user input by 10 
			mfhi		$t2				#Place the remainder in $t2
			mflo		$t1				#Place the quotient in $t1
			add		$t3, $t3, $t2		#Maintain the sum variable in register $t3
			j		itSum
			
print:		add		$a0, $t3, $zero		#Add the sum as argument to print call
			jal		PRINTSUMIT		#Print call which prints the resultant sum
			lw		$ra, 4($sp)		#Gets the return address and returns to the parent call
			lw		$s0, 0($sp)		#Gets the user input value stored on the stack
			addi		$sp, $sp, 8		#Pops the elements on the stack
			jr 		$ra				#Jumps to the original function
			
# -------------------------------------------------------------  FUNCTION FOR RECURSIVE CALCULATION --------------------------------------------------------

RECURSIVE: 	addi		$sp, $sp, -12		#Adds stack space
			sw		$ra, 0($sp)		#Places the user input and the current remainder which has to be adder in the stack
			sw		$s1, 4($sp)
			sw 		$s0, 8($sp)
						
			add		$t1, $a0, $zero			
			sle		$t0, $t1, 0		#Check for basecase where the resultant number is less than 0
			beq		$t0, 1, baseCase	#If it is 0 then jump to baseCase calculation and return
			
			div		$t1, $t1, 10		#Divide user input by 10 
			mfhi		$s1				#Place the remainder in $t2
			mflo		$a0				#Pass the quotient as the argument
			jal		RECURSIVE		#Compute recursively
			
			lw		$ra, 0($sp)		#After recursive step
			lw		$s1, 4($sp)		#Fetch values stored from the stack and add them up
			lw 		$s0, 8($sp)
			add		$v0, $v0, $s1		#Pass the computed sum as a recursive call return
			add		$sp, $sp, 12
			jr		$ra		
			
baseCase: 	lw		$ra, 0($sp)
			lw		$s1, 4($sp)
			lw 		$s0, 8($sp)
			add		$v0, $s1, $zero
			add		$sp, $sp, 12
			jr		$ra
			
			
# -------------------------------------------------------------  FUNCTION FOR PRINTING THE SUM  ITERATIVE ------------------------------------------------------------------

PRINTSUMIT:	addi 		$sp, $sp, -4
			sw		$ra, 0($sp)
			
			add		$t3, $a0, $zero
			li 		$v0, 4		#System call code for Print String
			la 		$a0, promptIt 	#Load address of promptSum into $a0
			syscall	
			
			li		$v0, 1		#System call to print 
			add		$a0, $t3, $zero				
			syscall
			
			lw		$ra, 0($sp)
			add		$sp, $sp, 4
			jr 		$ra
			
			
# -------------------------------------------------------------  FUNCTION FOR PRINTING THE SUM  RECURSIVE ------------------------------------------------------------------

PRINTSUMREC:	addi 		$sp, $sp, -4
			sw		$ra, 0($sp)
			
			add		$t3, $a0, $zero
			li 		$v0, 4		#System call code for Print String
			la 		$a0, promptRec 	#Load address of promptSum into $a0
			syscall	
			
			li		$v0, 1		#System call to print 
			add		$a0, $t3, $zero				
			syscall
			
			lw		$ra, 0($sp)
			add		$sp, $sp, 4
			jr 		$ra
			