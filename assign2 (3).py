#																				SPICE PROGRAM - PART 2
#																				M LAHARI [EE20B081]	
# Importing the necessary modules.
from numpy import *
from sys import argv, exit

# A function created to converted exponents to real numbers.
def converter(str):
	c = str.split('e')
	value = (float(c[0]))*(10**int(c[1]))
	return value

# Classes are needed to be declared for each component.
class Resistor:
	def __init__(self,name,n1,n2,value):
		self.name = name
		self.n1 = n2
		self.n2 = n1
		self.value = value

class Capacitor: 
	def __init__(self,name,n1,n2,value):
		self.name = name
		self.n1 = n2
		self.n2 = n1
		self.value = value

class Inductor:
	def __init__(self,name,n1,n2,value):
		self.name = name
		self.n1 = n2
		self.n2 = n1
		self.value = value

class VoltageSource:
	def __init__(self,name,n1,n2,value):
		self.name = name
		self.n1 = n2
		self.n2 = n1
		self.value = value		

class CurrentSource:
	def __init__(self,name,n1,n2,value):
		self.name = name
		self.n1 = n2
		self.n2 = n1
		self.value = value		


# If there isn't only 2 arguments then the program shows error.
if len(argv)!=2:
	print("Please provide the correct 2 arguments in the commandline.")
	exit()

# Assigning constants variables to .circuit and .end 
CIRCUIT = ".circuit"
END = ".end"
AC = ".ac"

try:

# Opening the file mentioned in the commandline.
	with open(argv[1]) as f:
		lines = f.readlines()

# These are parameters to check the errors in the file format. 		
		start = -1; start_check = -1; end = -2; end_check = -1; ac = -1 ; ac_check = -1

# The program will traverse through the file and take out only the required part.
		for line in lines:
			if CIRCUIT == line[:len(CIRCUIT)]:
				start = lines.index(line)
				start_check = 0

			elif END == line[:len(END)]:
				end = lines.index(line)
				end_check = 0
#This part is to check if the circuit has an AC or a DC source. 	
			elif AC == line[:len(AC)]:
				ac = lines.index(line)
				ac_check = 1
		
		if start >= end or start_check == -1 or end_check == -1:
			print("Invalid circuit definition.")
			exit()

# Creating a list and storing the necessary information into it.			
		l = [] ; k=0
# In case of an AC circuit, the required information is collected.		
		try:
			if ac_check ==1:
				_,ac_name,frequency = lines[ac].split("#")[0].split() 
				angular_frequency = 2*3.1415926536*converter(frequency)

			for line in (lines[start+1:end]):
				name,n1,n2,*value = line.split("#")[0].split()

				if name[0] == 'R':
					object = Resistor(name,n1,n2,value)

				elif name[0] == 'C':
					object = Capacitor(name,n1,n2,value) 

				elif name[0] == 'L':
					object = Inductor(name,n1,n2,value)
					
				elif name[0] == 'V':
					object = VoltageSource(name,n1,n2,value)
					k = k+1

				elif name[0] == 'I':
					object = CurrentSource(name,n1,n2,value)

# By using the converter() function, convert the values of the components into real numbers.
				if len(object.value) == 1:
					if object.value[0].isdigit() == 0:	
						object.value = float(converter(object.value[0]))
					else:
						object.value = float(object.value[0])	

# In case of an AC source, the voltage and phase are need to be assigned properly.
				else:
					object.value = (float(object.value[1])/2)*complex(cos(float(object.value[2])),sin(float(object.value[2])))			

				l.append(object)

# If the netlist is not written properly,then the program shows an error.
		except IndexError:
			print("Please make sure the netlist is written properly.")	
			exit()

# Nodes are creating using a dictionary.
	node ={}
	for object in l:
		if object.n1 not in node:
			if object.n1 == 'GND':
				node['n0'] = 'GND'

			else:	
				name = "n" + object.n1
				node[name] = int(object.n1)

		if object.n2 not in node:
			if object.n2 == 'GND': 
				node['n0'] = 'GND'

			else:	
				name = "n" + object.n2 	
				node[name] = int(object.n2)

	node['n0'] = 0			
	n = len(node)

# Creating the M and b matrices for solving the equations.
	M = zeros(((n+k-1),(n+k-1)),dtype="complex_")
	b = zeros(((n+k-1),1),dtype="complex_")
	p=0

# If it is an AC or a DC source,this part will find matrices M and b being considered.
	for object in l:

# In case of a resistor, the matrix M is filled in a certain way as shown below.		
		if object.name[0] == 'R':
			if object.n2 == 'GND': 
				M[int(object.n1)-1][int(object.n1)-1] += 1/object.value

			elif object.n1 == 'GND':
				M[int(object.n2)-1][int(object.n2)-1] += 1/object.value
					
			else:	
				M[int(object.n1)-1][int(object.n1)-1] += 1/object.value
				M[int(object.n2)-1][int(object.n2)-1] += 1/object.value
				M[int(object.n1)-1][int(object.n2)-1] += -1/object.value
				M[int(object.n2)-1][int(object.n1)-1] += -1/object.value

# In case of a capacitor, the impedance is calculated first and then the matrix M is filled.
		elif object.name[0] == 'C':
			if ac_check ==1:
				Xc = -1/(float(object.value)*angular_frequency)
				object.value = complex(0,Xc)

			if object.n2 == 'GND': 
				M[int(object.n1)-1][int(object.n1)-1] += 1/object.value
			elif object.n1 == 'GND':
				M[int(object.n2)-1][int(object.n2)-1] += 1/object.value
					
			else:	
				M[int(object.n1)-1][int(object.n1)-1] += 1/object.value
				M[int(object.n2)-1][int(object.n2)-1] += 1/object.value
				M[int(object.n1)-1][int(object.n2)-1] += -1/object.value
				M[int(object.n2)-1][int(object.n1)-1] += -1/object.value

# In case of an inductor, the impedance is calculated first and then the matrix M is filled.
		elif object.name[0] == 'L':
			if ac_check ==1:
				Xl = (float(object.value)*angular_frequency)
				object.value = complex(0,Xl)

			if object.n2 == 'GND': 
				M[int(object.n1)-1][int(object.n1)-1] += 1/object.value
			elif object.n1 == 'GND':
				M[int(object.n2)-1][int(object.n2)-1] += 1/object.value
					
			else:	
				M[int(object.n1)-1][int(object.n1)-1] += 1/object.value
				M[int(object.n2)-1][int(object.n2)-1] += 1/object.value
				M[int(object.n1)-1][int(object.n2)-1] += -1/object.value
				M[int(object.n2)-1][int(object.n1)-1] += -1/object.value

# In case of a current source, the matrix b is filled as shown.
		elif object.name[0] == 'I':
			if object.n2 == 'GND':
				b[int(object.n1)-1][0] += object.value

			elif object.n1 == 'GND':
				b[int(object.n2)-1][0] += -object.value

			else:
				b[int(object.n1)-1][0] += object.value
				b[int(object.n2)-1][0] += -object.value

# In case of a voltage source, the matrices M and b are filled as shown.
		elif object.name[0] == 'V':
			if object.n2 == 'GND':
				M[int(object.n1)-1][n-1+p] += 1
				M[n-1+p][int(object.n1)-1] += 1
				b[n-1+p] += object.value
				p = p+1			
			elif object.n1 == 'GND':
				M[int(object.n2)-1][n-1+p] += -1
				M[n-1+p][int(object.n2)-1] += -1
				b[n-1+p] += object.value
				p = p+1			
			else:	
				M[int(object.n1)-1][n-1+p] += 1
				M[int(object.n2)-1][n-1+p] += -1
				M[n-1+p][int(object.n1)-1] += 1
				M[n-1+p][int(object.n2)-1] += -1
				b[n-1+p] += object.value
				p = p+1

# The linalg.solve() function is used to solve the circuit equations.
	V = linalg.solve(M,b)

	print(V,"\n")			

	for o in range(n-1):
		print("V",o+1,"=",V[o],"\n")
	for q in range(k):
		print("I",q+1,"=",V[q+n-1],"\n")

# The program will throw in this error if the name of the netlist file is not proper 
# or if the netlist file is not found in the same directory as the program.

except FileNotFoundError:
	print("Invalid File.")
	exit()