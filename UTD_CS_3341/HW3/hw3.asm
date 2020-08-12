# Prompt the user for an integer in the range of 0 to 100. If the user inputs 0 the program stops.
# Otherwise, the program stores the numbers from 0 up to the input value into an array of words in memory, i.e. initializes the array with values from 0 up to N where N is the value that user has given
# The program then adds the value of all even numbers of the array together (up to N) by loading them from the main memory then add them up, then prints out the sum with the message "The sum of even integers from 0 to N is:". For example, if the user gave 6 as the input the program prints out "The sum of even integers from 0 to 6 is 12".			
						
									
			.data				#Indicates following data items are stored in the data segment
promptX: 		.asciiz	"\n Please input value for N between 0 and 100 "
promptSum:	.asciiz 	"\n The sum of even integers from 0 to N is: "
list:  			.word	100			# Space to store the words of integers

.text 				#Indicates items stored in the user text segment,[INSTRUCTIONS]
			.globl 	main			#Declare that main is global and can be referenced from other files
main:		
			la 		$a0, promptX 	#Load address of promptX into $a0
			li 		$v0, 4		#System call code for Print String
			syscall			
			li 		$v0, 5		#System call code for Read Integer
			syscall			
			move 	$t1, $v0		#Moving the user input of X  to register $t1
			beq		$t1, 0, exit
			
			add		$s1, $s1, 2	#Used to check the difference between N and current integer in the loop for sumnumbers
			add		$s3, $t1, 1	#Used in beq check condition of store numbers, to instruct to store all the numbers below N+1
			
			la		$t7, list		#t7 is the register where we store array
			add		$t6, $t7, $zero	#t6 is used while iterating to sum up numbers
storenumbers:	beq		$s0, $s3, sumnumbers	#If the current pointer is N+1 then no need to store, we can proceed to sumup evens
			sw		$s0, 0($t7)	#Store the integer in the address given by $t7
			addi		$s0, $s0, 1	#Increment value in $s0 till N+1, which starts from 0
			addi		$t7, $t7, 4	#Increment to the next word address
			j 		storenumbers	#Loop back to store numbers
						
sumnumbers:	sub		$t5, $t1, $t4	#Find the difference between N and the current pointer t4 initialized at 0
			slt		$t5, $t5, $s1	#If the difference between them is <2 then fill t5 accordingly
			beq		$t5, 1, printsum	#As the difference reached 1(Odd)or 0(even) we can proceed to printing the sum
			lw		$t4, 0($t6)	#Load the word currently stored in t6
			add		$t6, $t6, 8	#Increment the address by 8, as we only care about evens
			add		$t3, $t3, $t4	#Maintain the sum in t3
			j 		sumnumbers	#Loop to sum up the numbers
			
printsum:		li 		$v0, 4		#System call code for Print String
			la 		$a0, promptSum 	#Load address of promptSum into $a0
			syscall	
			
			li		$v0, 1		#System call to print 
			add		$a0, $t3, $zero				
			syscall
			
exit:			li 		$v0, 10		#Terminate program run 
			syscall				#Return control to system
