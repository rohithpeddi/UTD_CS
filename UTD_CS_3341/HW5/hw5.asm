			.data		#Indicates following data items are stored in the data segment
promptRound: 		.asciiz	"\n Please input number of round pizzas sold in a day: "
promptSquare: 	.asciiz	"\n Please input number of square pizzas sold in a day: "
promptEstimate: 	.asciiz	"\n Please estimate the total number of pizzas sold in day in a square foot : "
printTotal:		.asciiz	"\n Total number of pizzas sold in square feet : "
printRound:		.asciiz	"\n Total number of round pizzas sold in square feet : "
printSquare:		.asciiz	"\n Total number of sqaure pizzas sold in square feet : "
printYeah:		.asciiz	"\n YEAH !!"
printBummer:		.asciiz	"\n BUMMER !!"

const:			.float	0.00694, 3.14, 16.0

.text 				#Indicates items stored in the user text segment,[INSTRUCTIONS]
			.globl 	main			#Declare that main is global and can be referenced from other files
			
main:		la 		$a0, promptRound		#Load address of promptX into $a0
			li 		$v0, 4			#System call code for Print String
			syscall			
			li 		$v0, 5			#System call code for Read Integer
			syscall			
			move 	$s0, $v0			#Store the number of round pizzas sold in $s0
			
			la 		$a0, promptSquare	#Load address of promptX into $a0
			li 		$v0, 4			#System call code for Print String
			syscall			
			li 		$v0, 5			#System call code for Read Integer
			syscall			
			move 	$s1, $v0			#Store the number of square pizzas sold in $s1
			
			la 		$a0, promptEstimate#Load address of promptX into $a0
			li 		$v0, 4			#System call code for Print String
			syscall
			
			li $v0, 6					# Read float value
			syscall
			
					
			la		$t5, const
			lwc1		$f10, 0($t5)		#Load the conversion factor from sqaure inches to sqaure feet in $f10
			
			#compute square pizzas in square foot
			addi		$t1, $t1, 10		#Load the size of the sqaure pizza
			mult 		$t1, $t1			#Square the size of the sqaure pizza
			mflo		$t1				#Fetch the sqaured value from mflo(as it does not exceed 32 bit value)			
			mult		$t1, $s1			#Multiply the sqaured value with the number of square pizzas sold
			mflo		$t1				#Move the result to $t1 (assuming the result does not exceed 32 bit value)
			
			mtc1		$t1, $f1			#Move the sqaure inch value to floating point 
			cvt.s.w 	$f1, $f1			#Convert integer to float value
			mul.s	$f1, $f1, $f10		#Convert the sqaure inch value to sqaure feet
			
			mov.s	$f3, $f1			#Store the sqaure feet value for the sqaure pizza in  $f3			
			
			#compute round pizzas in square foot
			mtc1		$s0, $f2			#Move the number of round pizzas value to $f2
			cvt.s.w 	$f2, $f2			#Convert integer to float value
			lwc1		$f11, 4($t5)		#Load the constant value for pie
			mul.s	$f2, $f2, $f11		#Multiply the total number with pie
			lwc1 		$f11, 8($t5)		#Load the constant value for diameter sqaured
			mul.s	$f2, $f2, $f11		#Divide the result with 4
				
			mul.s	$f2, $f2, $f10		#Convert square inches to square foot
			
			# COMPUTING TOTAL			
			
			add.s	$f1, $f2, $f1		#Adding the value of the round pizza in square foot to the total	
			
			#PRINTING DETAILS OF  SIZES OF EACH TYPE OF PIZZA			
			la 		$a0, printTotal		#Load address of promptX into $a0
			li 		$v0, 4			#System call code for Print String
			syscall		
			
			mov.s  	$f12, $f1			#Move contents of the total to $f12, inorder to print 
			li 		$v0, 2 	
			syscall			

			la 		$a0, printRound	#Load address of promptX into $a0
			li 		$v0, 4			#System call code for Print String
			syscall		
			
			mov.s  	$f12, $f2			#Move contents of the total to $f12, inorder to print 
			li 		$v0, 2 	
			syscall			
			
			la 		$a0, printSquare	#Load address of promptX into $a0
			li 		$v0, 4			#System call code for Print String
			syscall		
			
			mov.s  	$f12, $f3			#Move contents of the total to $f12, inorder to print 
			li 		$v0, 2 	
			syscall			
			
			# PRINTING THE STATE OF THE SALE BY COMPARISON			
			
			c.le.s 	$f0, $f1			#$f1 stores the calculated the total square foot pizzas, $f0 stores the estimated total square foot pizza
			bc1f		BUMMER			# Estimated is greater than calculated
			bc1t    	YEAH			# Estimated is less than calculated		
			
			
YEAH:		la 		$a0, printYeah		#Load address of promptX into $a0
			li 		$v0, 4			#System call code for Print String
			syscall			
			j 		exit			
			
BUMMER:		la 		$a0, printBummer	#Load address of promptX into $a0
			li 		$v0, 4			#System call code for Print String
			syscall			
			j 		exit			
			
exit:			li 		$v0, 10		#Terminate program run 
			syscall				#Return control to system			