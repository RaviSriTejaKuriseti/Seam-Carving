# name: File path of the pgm image file
# Output is a 2D list of integers
def readpgm(name):
	image = []
	with open(name) as f:
		lines = list(f.readlines())
		if len(lines) < 3:
			print("Wrong Image Format\n")
			exit(0)

		count = 0
		width = 0
		height = 0
		for line in lines:
			if line[0] == '#':
				continue

			if count == 0:
				if line.strip() != 'P2':
					print("Wrong Image Type\n")
					exit(0)
				count += 1
				continue

			if count == 1:
				dimensions = line.strip().split(' ')
				print(dimensions)
				width = dimensions[0]
				height = dimensions[1]
				count += 1
				continue

			if count == 2:	
				allowable_max = int(line.strip())
				if allowable_max != 255:
					print("Wrong max allowable value in the image\n")
					exit(0)
				count += 1
				continue

			data = line.strip().split()
			data = [int(d) for d in data]
			image.append(data)
	return image	

# img is the 2D list of roundegers
# file is the output file path
def writepgm(img, file):
	with open(file, 'w') as fout:
		if len(img) == 0:
			pgmHeader = 'p2\n0 0\n255\n'
		else:
			pgmHeader = 'P2\n' + str(len(img[0])) + ' ' + str(len(img)) + '\n255\n'
			fout.write(pgmHeader)
			line = ''
			for i in img:
				for j in i:
					line += str(j) + ' '
				line += '\n'
			fout.write(line)

########## Function Calls ##########
#x = readpgm('test.pgm')			# test.pgm is the image present in the same working directory
#writepgm(x, 'test_o.pgm')		# x is the image to output and test_o.pgm is the image output in the same working directory
###################################
def average(image):
	W=(len(image[0]))
	H=(len(image))
	L=[[0 for u in range(W)] for v in range(H)]
	for i in range (0,H):
		for j in range (0,W):			
			if (i==0) or (j==0) or (i==H-1) or (j==W-1):						##Using the boundary conditions.
				L[i][j]=image[i][j]
			else:
				L[i][j]=round((image[i-1][j-1]+image[i-1][j]+image[i-1][j+1]+image[i][j-1]+image[i][j]+image[i][j+1]+image[i+1][j-1]+image[i+1][j]+image[i+1][j+1])/9)
																				##Making an average array.
	return L
			
a=readpgm('flower_gray.pgm')
b=average(a)
writepgm(b,'average.pgm')

def gradient_image(image):
	W=(len(image[0]))
	H=(len(image))
	grad=[[0 for c in range(W)] for d in range(H)]
	i=0																					##Initializing the boundary conditions for topmost row
	for j in range(1,W-1):
		h_diff=(image[H-1][j-1]-image[H-1][j+1])+2*(image[i][j-1]-image[i][j+1])+(image[i+1][j-1]-image[i+1][j+1])
		v_diff=(image[H-1][j-1]-image[i+1][j-1])+2*(image[H-1][j]-image[i+1][j])+(image[H-1][j+1]-image[i+1][j+1])
		grad[i][j]=round(((h_diff)**2 + (v_diff)**2)**0.5)
	j=0																					##Initializing the boundary conditions for leftmost column
	for i in range(1,H-1):
		h_diff=(image[i-1][W-1]-image[i-1][j+1])+2*(image[i][W-1]-image[i][j+1])+(image[i+1][W-1]-image[i+1][j+1])
		v_diff=(image[i-1][W-1]-image[i+1][W-1])+2*(image[i-1][j]-image[i+1][j])+(image[i-1][j+1]-image[i+1][j+1])
		grad[i][j]=round(((h_diff)**2 + (v_diff)**2)**0.5)

	i=H-1																				##Initializing the boundary conditions for bottommost row
	for j in range(1,W-1):
		h_diff=(image[i-1][j-1]-image[i-1][j+1])+2*(image[i][j-1]-image[i][j+1])+(image[0][j-1]-image[0][j+1])
		v_diff=(image[i-1][j-1]-image[0][j-1])+2*(image[i-1][j]-image[0][j])+(image[i-1][j+1]-image[0][j+1])
		grad[i][j]=round(((h_diff)**2 + (v_diff)**2)**0.5)
	j=W-1																				##Initializing the boundary conditions for rightmost column
	for i in range(1,H-1):
		h_diff=(image[i-1][j-1]-image[i-1][0])+2*(image[i][j-1]-image[i][0])+(image[i+1][j-1]-image[i+1][0])
		v_diff=(image[i-1][j-1]-image[i+1][j-1])+2*(image[i-1][j]-image[i+1][j])+(image[i-1][0]-image[i+1][0])
		grad[i][j]=round(((h_diff)**2 + (v_diff)**2)**0.5)

	 
	h_diff0=(image[H-1][W-1]-image[H-1][1])+2*(image[0][W-1]-image[0][1])+(image[1][W-1]-image[1][1])
	v_diff0=(image[H-1][W-1]-image[1][W-1])+2*(image[H-1][0]-image[1][0])+(image[H-1][1]-image[1][1])		
	grad[0][0]=round(((h_diff0)**2 + (v_diff0)**2)**0.5)								##Initializing the boundary conditions for top-left corner

	h_diff1=(image[H-1][W-2]-image[H-1][0])+2*(image[0][W-2]-image[0][1])+(image[1][W-2]-image[1][1])
	v_diff1=(image[H-1][W-2]-image[1][W-2])+2*(image[H-1][0]-image[1][0])+(image[H-1][0]-image[1][0])		
	grad[0][W-1]=round(((h_diff1)**2 + (v_diff1)**2)**0.5)							##Initializing the boundary conditions for top-right corner

	h_diff2=(image[H-2][W-1]-image[H-2][1])+2*(image[H-1][W-1]-image[H-1][1])+(image[0][W-1]-image[0][1])
	v_diff2=(image[H-2][W-1]-image[0][W-1])+2*(image[H-2][0]-image[0][0])+(image[H-2][1]-image[0][1])
	grad[H-1][0]=round(((h_diff2)**2 + (v_diff2)**2)**0.5)							##Initializing the boundary conditions for bottom-left corner

	h_diff3=(image[H-2][W-2]-image[H-2][0])+2*(image[H-1][W-2]-image[H-1][0])+(image[0][W-2]-image[0][0])
	v_diff3=(image[H-2][W-2]-image[0][W-2])+2*(image[H-2][W-1]-image[0][W-1])+(image[H-2][0]-image[0][0])
	grad[H-1][W-1]=round(((h_diff3)**2 + (v_diff3)**2)**0.5)																
																					##Initializing the boundary conditions for bottom-right corner

	for i in range(1,H-1):
		for j in range(1,W-1):
				h_diff=(image[i-1][j-1]-image[i-1][j+1])+2*(image[i][j-1]-image[i][j+1])+(image[i+1][j-1]-image[i+1][j+1])
				v_diff=(image[i-1][j-1]-image[i+1][j-1])+2*(image[i-1][j]-image[i+1][j])+(image[i-1][j+1]-image[i+1][j+1])
				grad[i][j]=round(((h_diff)**2 + (v_diff)**2)**0.5)
	
	
	maxim=0
	for a in range(0,H):
		for b in range(0,W):
			if(maxim<grad[a][b]):
				maxim=grad[a][b]									##Getting the maximum of array
					

	for i in range(0,H):
		for j in range(0,W):
			grad[i][j]=round((grad[i][j]*255)/maxim)				##Scaling the array to 255/maxim times
				
	return grad

c=readpgm('flower_gray.pgm')
d=gradient_image(c)
writepgm(d,'edge.pgm')

def edgedetection(image):
	W=(len(image[0]))
	H=(len(image))
	Minindex=[]
	L1=[]
	for j in range(0,W):
		L1.append(image[0][j])
	Minindex.append(L1)
	
	for i in range(1,H):
		L=[image[i][0]+min(Minindex[i-1][0],Minindex[i-1][1])]
		for j in range(1,W-1):
			L.append(image[i][j]+min(Minindex[i-1][j-1],Minindex[i-1][j],Minindex[i-1][j+1]))
		L.append(image[i][W-1]+min(Minindex[i-1][W-2],Minindex[i-1][W-1]))
		Minindex.append(L)

	return Minindex											##Forming the energy array using dynamic programming.

e=readpgm('edge.pgm')
f=edgedetection(e)
writepgm(f,'energy.pgm')

def careadd(L,e):
	if e not in L:
		L.append(e)										

def tracingpath(image,i,L):
	W=len(image[0])
	if(i==0):
		return L
	else:
		for e in L:
			if(e[0]==i):
				j=e[1]
				if (j!=0) and (j!=W-1):
					p=min(image[i-1][j-1],image[i-1][j],image[i-1][j+1])
					if(p==image[i-1][j-1]):
						careadd(L,([i-1,j-1]))
					if(p==image[i-1][j]) :
						careadd(L,([i-1,j]))
					if(p==image[i-1][j+1]):
						careadd(L,([i-1,j+1]))
				if(j==0):
					p=min(image[i-1][j],image[i-1][j+1])
					if(p==image[i-1][j]) :
						careadd(L,([i-1,j]))
					if(p==image[i-1][j+1]) :
						careadd(L,([i-1,j+1]))
				if(j==W-1):
					p=min(image[i-1][j-1],image[i-1][j])
					if(p==image[i-1][j-1]) :
						careadd(L,([i-1,j-1]))
					if(p==image[i-1][j]) :
						careadd(L,([i-1,j]))
		return tracingpath(image,i-1,L)	
															##Storing the path traced to get the least energy in a list.

def white(image):
	a=min(image[len(image)-1])
	M=[]
	for j in range(0,len(image[0])):
		if(image[len(image)-1][j]==a):
			M.append([len(image)-1,j])
	return tracingpath(image,len(image)-1,M)					##Returning the stored path.

def finalize(image,N):
	for e in N:
		image[e[0]][e[1]]=255									##Modifying the pixels in the initial image.
	return image

g=readpgm('energy.pgm')
h=readpgm('flower_gray.pgm')
i=finalize(h,white(g))
writepgm(i,'final.pgm')




	

		

		
