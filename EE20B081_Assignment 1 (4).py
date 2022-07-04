#																				SPICE PROGRAM - PART 1
#																				MONDI LAHARI[EE20B081]	
# Importing the necessary modules.
from sys import argv, exit

# if there isn't exactly 2 arguments commandline then program shows an error.
if len(argv)!=2:
	print("Only 2 arguments in the commandline.")
	exit()

# Assigning constants variables to .circuit and .end 
CIRCUIT = ".circuit"
END = ".end"

try:

# Opening the file mentioned in the commandline.
#(Answer to 1st point)
	with open(argv[1]) as f:
		lines = f.readlines()

# These are parameters to check the errors in the file format. 		
		start = -1; start_check = -1; end = -2; end_check = -1 

# The program will traverse through the file and take out only the required part.
#(4th question point)
		for line in lines:
			if CIRCUIT == line[:len(CIRCUIT)]:
				start = lines.index(line)
				start_check = 0;

			elif END == line[:len(END)]:
				end = lines.index(line)
				end_check = 0;

# The program will throw in an error if the circuit definition format is not proper.		
		if start >= end or start_check == -1 or end_check == -1:
			print("Invalid circuit definition.")
			exit()
			
# These lines of code will reverse and print the required result.
#(Answer to 5th point)
		for lines in reversed(lines[start+1:end]):
			c=reversed(lines.split('#')[0].split())	
			c = "  ".join(c)
			print(c)

# if the name of the netlist file is not proper, the program will throw in this error 
# even if the netlist file is not found in the same directory as the program.

except FileNotFoundError:
	print("Invalid File.")
	exit()
