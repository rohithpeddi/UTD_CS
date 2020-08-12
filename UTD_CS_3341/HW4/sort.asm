


main:
    			la  $t0, 24      			#base address of  Array into $t1
    			add $t0, $t0, 20    		# 4 bytes per int * 10 ints = 20 bytes    
                          
Loop1:             
    			add $t1, $0, $0     		# $t1 holds a flag to determine when the list is sorted
    			la  $a0, 24      			# Set $a0 to the base address of the Array

Loop2:         
    			lw  $t2, 0($a0)         		# sets $t0 to the current element in array
    			lw  $t3, 4($a0)         		# sets $t1 to the next element in array
    			slt $t5, $t2, $t3       		# $t5 = 1 if $t0 < $t1
    			beq $t5, $0, CONTINUE   	# if $t5 = 1, then swap them
    			add $t1, $0, 1          	# if we need to swap, we need to check the list again
    			sw  $t2, 4($a0)         	# store the greater number in the higher position in array (swap)
    			sw  $t3, 0($a0)         	# store the lesser number in the lower position in array (swap)

CONTINUE:
    			addi $a0, $a0, 4            	# advance the array to start at the next location from last time
    			bne  $a0, $t0, Loop2   	# If $a0 != the end of Array, jump back to Loop2
    			bne  $t1, $0, Loop1    	# $t1 = 1, another pass is needed, jump back to Loop1