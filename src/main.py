# import important libraries and files

import cv2 as cv
import os
import math
import imutils 
import copy
#------------------------------------------------------
# create windows

windowName = "Input Image";#window name
cv.namedWindow(windowName, cv.WINDOW_NORMAL); # create input window 

#------------------------------------------------------
points = []
resized_image1 =[]
drawing = False # true if mouse is pressed
ix,iy = -1, -1
fx,fy = -1, -1
line_count =0
real_measurement_in_image_name = False
def calculate_dist( point1, point2):
	# print("in dist: " ,point1,point2)
	try:
		px,py= point1
		nx,ny= point2
	except:
		return 1000

	comp_x_sqr = math.pow(nx-px,2)
	comp_y_sqr = math.pow(ny-py,2)
	
	dist= math.sqrt(comp_x_sqr + comp_y_sqr )
	print(dist)
	return dist



# mouse callback function
def mouse_callback(event,x,y,flags,param):
	global ix, iy, drawing, points, line_count
	lineThikness=3
	color=(255,0,0) if line_count == 0 else (0, 0, 255)
	img = resized_image1
	if event == cv.EVENT_LBUTTONDOWN:
		drawing = True
		ix,iy = x,y
		points.append((ix,iy))

	elif event == cv.EVENT_MOUSEMOVE:
		img = copy.deepcopy(resized_image1)
		if drawing == True:
			cv.line(img,(ix,iy),(x,y),color,lineThikness)
			

	elif event == cv.EVENT_LBUTTONUP:
		drawing = False
		fx,fy = x,y
		cv.line(img,(ix,iy),(x,y),color,lineThikness)
		points.append((fx,fy)) 
		if len(points) == 4:
			antenna_pixel_height = calculate_dist(points[0],points[1])
			building_height = calculate_dist(points[2],points[3]) 
			
			if real_measurement_in_image_name:
				real_to_pixel_ratio = real_dis/building_height
			else:
				real_building_height = float(input('Enter building\'s real height: '))
				real_to_pixel_ratio = real_building_height/building_height
			
			real_antenna_height = real_to_pixel_ratio * antenna_pixel_height
			print('Antenna\'s real length: ',real_antenna_height,' m')
			points =[]
		line_count +=1
		if line_count == 2:
			line_count =0
	cv.imshow(windowName,img)


cv.setMouseCallback(windowName, mouse_callback)
cwd = os.getcwd()

print('How to use?\n\
					step1: draw a line along the object you want to measure(target).\n\
					step2: draw a line along the reference object.\n\
					step3: if the real length of the reference object is not provided\n\
						through	the name of the image, you will be promoted to enter \n\
						it through the terminal. Please note that it has to be in meters.\n\
					step4: the approximated length of the target object will be printed out in the terminal.\n\
					step5: press any key to move to the next image or repeat the previous steps to retake\
the measurements of the current image') 

if cwd.split('/')[-1] == 'src':
	cwd= os.path.join(cwd,'..')

path = os.path.join(cwd,'data')
available_images = os.listdir(path)

for img in available_images:
	global real_dis
	real_dis = float(img.split('.')[0].replace('_','.'))
	image = cv.imread(os.path.join(path,img))
	resized_image = imutils.resize(image, width=600)
	resized_image1 = copy.deepcopy(resized_image)
	cv.imshow(windowName,resized_image)
	k = cv.waitKey(0)
	if k == 27:         # wait for ESC key to exit
		if img == available_images[-1]:
			cv.destroyAllWindows()
		else:
			continue






        
