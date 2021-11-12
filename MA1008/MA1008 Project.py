import math
import turtle
import os
import datetime
import sys

def path(): #Gets the path of the python program and returns it
    return os.path.dirname(os.path.realpath(__file__))

def file_check(): #Checks if text files exist in the python folder, raises error if not
    count = 0
    files = []
    for file in os.listdir(path()): #Checks through all files
        if file.endswith(".txt"): #Only want files with .txt extention
            files.append(file) #Adds to list
            count += 1
    if count == 0: #No .txt files found
        raise ValueError("no file")
    return files

def clearConsole(): #OS clear command, works for linux or windows
    command = 'clear' #Clears console
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

def date_time(): #Returns formated date and time
    now = datetime.datetime.now()
    return now.strftime( "%d/%m/%Y %H:%M:%S" )

def new_file( segment_no, base_radius, follower_radius ): #Writes data to a new file, can overwrite files if desired. Other datas dont need to be passed as they are list form
    while True:
        try:
            name = input("Name of file? (include .txt)")
            f = open(name, "x+") #Tries to create a new .txt file, raises error if file already exists
            break
        except:
            while True:
                choice = input('File already exists. Enter y to continue or n to return.\n')
                if choice.lower() == "y": #If want to overwrite
                    f = open(name, "w+") #Opens file to overwrite
                    break
                elif choice.lower() == "n": #Returns to start in order to try a different name
                    break
                else: #Invalid values
                    invalid_input()
                    continue

    f.write(f"Last edited on: {date_time()}\n") #Header line
    f.write(f"Total Number of Segment: {segment_no:n} Radius of Base Circle: {base_radius:n} Radius of Follower: {follower_radius:n}\n") #Header line
    f.write(f"{'Segment No':^14s}{'Motion Type':^15s}{'Angular Range':^17s}{'Curve Shape':^15s}{'Displacement(mm)':^20}"+"\n") #Header line
    for i in range(1,segment_no + 1, 1): #Writes data line by line
        f.write(f"{i:^14n}{motion_type[i]:^15n}{angular_range[i]:^17n}")
        if motion_type[i] == 2 or motion_type[i] == 3:
            f.write(f"{curve_type[i]:^15n}{displacement[i]:^20n}\n")
        else:
            f.write(f"{'-':^15s}{displacement[i]:^20n}\n")
    f.close() #Closes file to save when done

def read_file(): #Reads lines of file into content_of_file, resets cursor for future use
    files = file_check() #Checks for txt file in python program directory
    while True:
        try:
            print("The following files are available:\n")
            for i in range(len(files)): #Prints list of available files
                print(f"{i + 1}. {files[i]}\n")
            file_no = int(input("Enter file number: ")) #Gets file choice
            if file_no == 0 or file_no > (len(files)): #Invalid value testing
                raise ValueError("out of range")
            f = open(files[file_no - 1],"r")
            content_of_file = f.readlines() #Reads file contents to variable
            f.seek(0,0) #Returns pointer to start of file
            f.close() #Closes file
            return content_of_file
        except ValueError as e:
            error_sorter(e)

def data(angular_range, curve_type, motion_type, displacement): #Collects the data from either file or user input
    content_of_file = [0]
    while True:
        data_choice = input("Would you like to enter parameters or read from a file? \n1:File\n2:New\n")
        if data_choice =="2": #New set of values
            segment_no = segment_input()
            for i in range(1,segment_no+1): #Number of cycles depends on entered segment_no
                motion_type.append(motion(i))
                angular_range.append(range_angle(i))
                if int(motion_type[i]) == 1: #Dwell type, so no curve or displacement
                    curve_type.append(0)
                    displacement.append(0)
                else: #Normal operation
                    curve_type.append(curve(i))
                    displacement.append(height(i))
            base_radius = base_input()
            follower_radius = follower_input()
            return segment_no, base_radius, follower_radius, data_choice #End

        elif data_choice == "1": #Read from file
            content_of_file = read_file() #Reads file content
            for i in content_of_file: #Prints data for user to check
                print(i)
            while True:
                correct = input("Is the data correct (y/n)?\n") #Check if data read was correct
                if correct.lower() == "n" or correct.lower() == "y": #Data correct so exit error checker loop
                    break
                else:
                    invalid_input()
            if correct.lower() == "n": #If not correct, restarts the loop
                 continue
            Line1 = content_of_file[1] #Line 1 has the details of the data
            Line1 = Line1.split(" ") #Splits based on " "
            Line1[-1] = Line1[-1].rstrip() #Strips the trailing spaces
            segment_no = int(Line1[4])
            base_radius = int(Line1[9])
            follower_radius = int(Line1[13])
            for j in range(3, segment_no+3): #Reads the rest of the lines and splits then sorts the data
                Line = content_of_file[j]
                Line = Line.split(" ") #Splits string based on spaces
                while ('' in Line): #Removes blank indexes in the string
                    Line.remove("")
                while ('\n' in Line): #Removes end line character
                    Line.remove("\n")
                motion_type.append(int(Line[1]))
                angular_range.append(int(Line[2]))
                if Line[1] == '1': #Checking for dwell motion
                    curve_type.append(0) #No curve or displacement cause dwell motion
                    displacement.append(0)
                else: #Either rise or return
                    curve_type.append(int(Line[3]))
                    displacement.append(int(Line[4]))
            return segment_no, base_radius, follower_radius, data_choice #End
        elif data_choice == '': #Empty line error
            empty_input()
        else: #Other errors
            invalid_input()

def invalid_input(): #Prints "Invalid input. Check again."
    print("\nInvalid input. Try again.\n")

def invalid_value(): #Prints "That was not a valid value. Try again."
    print("\nThat was not a valid value. Try again.\n")

def empty_input(): #Prints "Empty input. Try again."
    print("Empty input. Try again.\n")

def negative_input(): #Value cannot be negative.
    print("\nValue cannot be negative.\n")

def integre_only(): #Please input integres only.
    print("\nPlease input integres only.\n")

def file_error(): #Prints "Values in file have errors."
    print("\nValues in file have errors.\n")

def not_exist():
    print("\nNo text files exist in the directory. Move data file where program is before trying again\n")

def restart():
    print("\nRestarting\n")

def error_sorter(e = ''): #Checks input e which is error type and prints error message accordingly
    error = str(e)
    if error == 'float input': #Float entered
        integre_only()
    elif error == 'empty': #Empty input
        empty_input()
    elif error == 'negative input': #Negative number entered
        negative_input()
    elif error == 'out of range': #Invalid values
        invalid_value()
    elif error == 'file error':
        file_error()
    elif error == 'no file': #No txt files exist
        not_exist()
    elif error == 'restart':
        restart()
    else: #When a string or letters are entered instead of numbers.
        invalid_input()

def pi(x=0): #Returns pi value, either *1 or *2
    if x == 1:
        return math.pi #Value pi
    elif x == 2:
        return math.tau #Value of 2 * pi using tau

def segment_input(): #Gets number of motion segments
    while True:
        try:
            segment = float(input("Number of motion segments: "))
            if not segment: #Empty input
                raise ValueError('empty')
            elif segment.is_integer() == False: #If value has decimals, it cannot be accepted
                raise ValueError("float input")
            elif segment <= 1: #0 or less cannot exist
                raise ValueError("out of range")
            break #Exits when values are good
        except ValueError as e: #Dealing with known errors
            error_sorter(e)
    return int(segment)

def range_angle(i): #Gets input of segment range angle, i is segement no
    while True: #Error check for invalid inputs and invalid values
        try:
            range = float(input("Angular range of segment " + str(i) + ": ")) #Float to check for decimal degrees
            if not range: #Empty input
                raise ValueError('empty')
            elif range.is_integer() == False: #If value has decimals, it cannot be accepted
                raise ValueError("float input")
            elif range <= 0 : #Range cannot be negative
                raise ValueError("negative input")
            break #Exits when values are good
        except ValueError as e: #Dealing with known errors
            error_sorter(e)
    return int(range) #End

def motion(i): #input motion type, i is segement no
    while True:
        try:
            motion = float(input("Type of motion for segment " + str(i) + "\n '1' for Dwell \n '2' for Rise \n '3' for Return \n Choice: ")) #Float to check for decimal degrees
            if motion.is_integer() == False: #If value has decimals, it cannot be accepted
                raise ValueError("float input")
            elif not motion:
                raise ValueError('empty')
            elif motion == 1 or motion == 2 or motion == 3: #Only 1, 2 or 3 are valid inputs
                break #Exits when values are good
            else: #Everything else is invalid value
                raise ValueError("out of range")
        except ValueError as e: #Dealing with known errors
            error_sorter(e)
    return int(motion) #End

def curve(i): #Input curve type, i is segement no
    while True:
        try:
            curve = float(input("Type of curve for segment" + str(i) + "\n '1' for Constant acceleration \n '2' for Simple harmonic \n '3' for Cycloidal \n Choice: ")) #Float to check for decimal degrees
            if curve.is_integer() == False: #If value has decimals, it cannot be accepted
                raise ValueError("float input")
            elif not curve:
                raise ValueError('empty')
            elif curve == 1 or curve == 2 or curve == 3: #Only 1, 2 or 3 are valid inputs
                break #Exits when values are good
            else: #Everything else is invalid value
                raise ValueError("out of range")
        except ValueError as e: #Dealing with known errors
            error_sorter(e)
    return int(curve) #End

def height(i): #input motion height/displacement, i is segement no
    while True:
        try:
            height_input = float(input("Height/displacement of segment "+ str(i) + " in mm: "))
            if not height_input: #Empty input
                raise ValueError('empty')
            elif height.is_integer() == False: #If value has decimals, it cannot be accepted
                raise ValueError("float input")
            elif height_input >= 0:
                raise ValueError('negative_input')
            break #Success
        except ValueError as e: #Dealing with known errors
            error_sorter(e)
    return int(height_input)

def base_input(): #Gets base radius
    while True:
        try:
            base = float(input("Base circle radius: "))
            if not base:
                raise ValueError("empty")
            elif base <= 0:
                raise ValueError("negative input")
            break #Success
        except ValueError as e: #Dealing with known errors
            error_sorter(e)
    return int(base)

def follower_input(): #Gets follower radius
    while True:
        try:
            follower = int(input("Follower radius: "))
            if not follower:
                raise ValueError("empty")
            elif follower <= 0:
                raise ValueError("negative input")
            return follower
        except ValueError as e: #Dealing with known errors
            error_sorter(e)

def reset_var(): #Resets data variables
    return [0] , [0] , [0] , [0]

def curve_variables(i = 0, scale = 1): #Declares all varibles needed for displacement curves
    B = angular_range[i] #Gets range of the segment
    y_start = t.ycor() #Starting y coord
    h = displacement[i] #Gets the height
    y_end = t.ycor() - h * scale #Ending y coord for use when return
    return B, y_start, h, y_end

def constant_acceleration( i , direction = 1 , scale = 1 , yorigin = 0 ): # Direction = 1 is rising, direction = 2 is returning
    B, y_start, h, y_end = curve_variables( i , scale )
    for x in range( 1 , B + 1 ):
        if direction == 1: # Rising
            if x < B / 2: # First half
                y = y_start + 2 * h * ( x / B ) ** 2 * scale
                turtle_draw(t.xcor() + 1 , y )
            elif x >= B / 2: # Second half
                y = y_start + h * ( 1 - 2 * ( ( 1 - ( x / B ) ) ** 2 ) ) * scale
                turtle_draw(t.xcor() + 1,y)
        elif direction == 2: # Returning
            if x < B / 2: # First half
                y = y_end + h * ( 1 - 2 * ( x / B ) ** 2 ) * scale
                turtle_draw(t.xcor() + 1 , y )
            elif x >= B / 2: # Second half
                y = y_end + 2 * h * ( ( 1 - ( x / B ) ) ** 2 ) * scale
                turtle_draw(t.xcor() + 1 , y )
        R_list.append( ( y - yorigin ) / scale ) #Adds non scaled displacement to the list

def simple_harmonic(i, direction = 1, scale = 1, yorigin = 0): # Direction = 1 is rising, direction = 2 is returning
    B, y_start, h, y_end = curve_variables(i,scale)
    for x in range(1,B+1):
        if direction == 1: # Rising
            y = y_start + h * ( ( 1 - math.cos( ( pi(1) * x ) / B ) ) / 2 ) * scale
            turtle_draw(t.xcor() + 1, y)
        elif direction == 2: # Returning
            y = y_end + h * ( ( 1 + math.cos( ( pi(1) * x ) / B ) ) / 2 ) * scale
            turtle_draw(t.xcor() + 1, y)
        R_list.append((y - yorigin)/scale) #Adds non scaled displacement to the list

def cycloidal_motion(i, direction = 1, scale = 1, yorigin = 0): # Direction = 1 is rising, direction = 2 is returning
    B, y_start, h, y_end = curve_variables(i,scale)
    for x in range(1,B+1,1):
        if direction == 1: # Rising
            y = y_start + h * (( x / B ) - math.sin((pi(2) * x) / B) / (pi(2))) * scale
            turtle_draw(t.xcor() + 1, y)
        elif direction == 2: # Returning
            y = y_end + h * (1 -  x / B  + math.sin((pi(2) * x) / B) / (pi(2))) * scale
            turtle_draw(t.xcor() + 1, y)
        R_list.append((y - yorigin)/scale) #Adds non scaled displacement to the list

def dwell(i = 0, scale = 1, yorigin = 0): #Dwell so the line just moves forward, no direction
    B, y_start, h, y_end = curve_variables(i,scale)
    turtle_draw(t.xcor() + B, t.ycor())
    for i in range(B):
        R_list.append((t.ycor()-yorigin)/scale) #Adds non scaled displacement to the list

def turtle_setup(): #Setup for turtle screen and world coordinates
    screen = turtle.Screen() #Screen initialisation
    screen.setup(840+4,440+8) #The +8 accounts for space taken up by title box and stuff
    screen.setworldcoordinates(-40,-40,800,400) #To get a margin around the sides
    t = turtle.Turtle() #Turtle initialisation #Clears the turtle window of previous drawings if any
    t.hideturtle() #Hides turtle
    t.speed(1) #Use 1 for testing/debug, 10 for normal use
    return t

def turtle_move(x = 0, y = 0): #Pen Up, goes to coordinates then Pen Down
    t.penup()
    t.goto(x, y)
    t.pendown()

def turtle_draw(x = 0, y = 0): #Moves turtle and draws line to coordinate
    t.goto(x, y)

def turtle_draw_line(x_start, y_start, x_end, y_end):
    turtle_move(x_start, y_start)
    turtle_draw(x_end, y_end)

def turtle_graph(): #Draws the x and y axis
    t.color('black')
    t.goto(0,0) #IDK why but its needed
    turtle_move(0,0)
    t.setheading(0) #Point to the right
    t.forward(380) #X axis line
    t.stamp()
    turtle_move(100, -35) #Writing position below x axis line
    t.write("Angle of rotation (degree)")
    turtle_move(0,0)
    t.setheading(90) #Point upwards
    t.forward(380) #Y axis line
    t.stamp()
    turtle_move(-15,385) #Writing position above y axis line
    t.write("Displacement (mm)")


def displacement_graph(xorigin = 0, yorigin = 0, scale = 1, segment_no = 0): #Draws displacement graph
    global R_list
    R_list = [0] #List of displacements across whole range
    turtle_move(xorigin,yorigin) #Sends turtle to origin of the graph
    for i in range(1 , segment_no+1):
        if motion_type[i] == 2: #Rise motion
            if curve_type[i] == 1:
                constant_acceleration(i, 1, scale, yorigin)
            elif curve_type[i] == 2:
                simple_harmonic(i, 1, scale, yorigin)
            elif curve_type[i] == 3:
                cycloidal_motion(i, 1, scale, yorigin)
        elif motion_type[i] == 3: #Return motion
            if curve_type[i] == 1:
                constant_acceleration(i, 2, scale, yorigin)
            elif curve_type[i] == 2:
                simple_harmonic(i, 2, scale, yorigin)
            elif curve_type[i] == 3:
                cycloidal_motion(i, 2, scale, yorigin)
        elif motion_type[i] == 1:
            dwell(i, scale, yorigin)

def min_max_checker():
    min = 0
    max = 0
    x = 0
    for i in range(1, segment_no+1):
        if motion_type[i] == 1:
            continue
        elif motion_type[i] == 2: #If rise then increase
            x += displacement[i]
        elif motion_type[i] == 3: #If return then decrease
            x -= displacement[i]
        if x < min:
            min = x
        if x > max:
            max = x
    origin = (abs(min)/abs(max-min))*360 #Finds the height of the y axis for 0, default is 0
    scale = 1 / (abs(max-min)/360) #Gets scale to multiply graph values
    return min, max, origin, scale

def graph_axis(x_min = 0, x_max = 360, y_min = 0, y_max = 360):
    x_range = abs(x_max - x_min) #Max range
    y_range = abs(y_max - y_min) #Max range
    x_step = 30 #Degree per axes along x axis
    turtle_move()#resets to origin 0,0
    for j in range( ( x_range // x_step ) + 1 ): #X axis axes values
        turtle_move( j * x_step , -20)
        t.write(f"{x_min + j * x_step:.0f}", align = "center")
        turtle_draw_line( j * x_step, -5, j * x_step , 5)
    for i in range( 7 ): #Y axis axes values
        turtle_move(-20, i*60)
        t.write( f"{y_min + i * (y_range/6):.0f}", align = "center")
        turtle_draw_line(-5 , i*60 , 5 , i*60 )

def data_check(): #Checks whether displacement and angular range is valid ie displacement at end = 0 and angular range sum = 360
    range_sum = 0
    height_sum = 0
    fault = 0
    for index, height in enumerate(displacement): #If rise then add displacement, if return then minus displacement
        if motion_type[index] == 2:
            height_sum += height
        if motion_type[index] == 3:
            height_sum -= height
        if height_sum < 0: #If the displacement goes into negative
            fault = 1
    if fault == 1: #Checks if the user intended for this behaviour
        while True:
            error = input("The displacement of the cam goes into the negatives, do you want to proceed? (y/n)\n")
            if error.lower() == 'y': #If intended, continue
                break
            elif error == 'n': #Not intended, break and restart the input
                raise ValueError("restart")
            else: #Error
                invalid_input()
    for i in range(1, len(angular_range)): #Adds total range together
        range_sum += angular_range[i]
    if math.isclose(range_sum,360) == True and math.isclose(height_sum,0) == True : #Checks if total range == 360 and final displacement == 0
        return True
    if math.isclose(range_sum,360) == False: #When total range =|= 360
        print("Angular range of segments does not add up to 360 degrees.")
    if math.isclose(height_sum,0) == False: #When displacement final =|= 0
        print("Displacement does not return to 0")
    if data_choice == "1": #If input was from file, say that file is invalid
        raise ValueError("file error")
    return False

def drawing( x_origin , y_origin , base_radius , follower_radius , scale ): #Calls functions to draw cam follower
    follower_circle( x_origin , y_origin , base_radius , follower_radius , scale )
    cam_profile( x_origin , y_origin , base_radius , follower_radius , scale )
    base_circle( x_origin , y_origin , base_radius , scale )
    pitch_circle( x_origin , y_origin , base_radius , follower_radius , scale )
    pitch_curve( x_origin , y_origin , base_radius , follower_radius , scale )
    turtle_move( 500 , -35)
    t.write(f"Base radius: {base_radius}mm", align = "center")
    turtle_move( 700 , -35)
    t.write(f"Follower radius: {follower_radius}mm", align = "center")

def scale_factor(): #Gets scaling factor for drawing
    max_displacement = max(R_list) #Returns max displacement
    scale = ( base_radius + follower_radius + max_displacement ) / 190 #Restricting max per side to 190 as thats the space allocated, stops it from overlapping since total space is 200
    return scale

def base_circle( x_origin , y_origin , base_radius , scale = 1 ): #Draws the base circle
    turtle_move( x_origin + ( base_radius / scale ) , y_origin )
    t.color('black')
    t.setheading( 90 ) #Draws circle on the left
    for i in range( 0 , 360 , 15 ): #Dashed circle
        if i % 2 == 0:
            t.penup()
        elif i % 2 != 0:
            t.pendown()
        t.circle(radius = (base_radius / scale), extent = 15) #Every 15 degrees, changes between penup and pendown

def pitch_circle( x_origin , y_origin , base_radius , follower_radius , scale = 1 ): #Draws the pitch circle
    radius = ( base_radius + follower_radius ) / scale
    t.color('black')
    turtle_move( x_origin + ( radius ) , y_origin )
    t.setheading( 90 )
    for i in range( 0 , 360 , 5 ):
        if i % 2 == 0:
            t.penup()
        elif i % 2 != 0:
            t.pendown()
        t.circle(radius = radius , extent = 5)

def follower_circle( x_origin , y_origin , base_radius , follower_radius , scale = 1 ): #Draws the follower circle
    turtle_move( x_origin + ( base_radius / scale ), y_origin ) #Moves to start point
    t.color('green')
    t.begin_fill()
    t.setheading( 270 ) #Draws a circle on the right
    t.circle( follower_radius / scale )
    t.end_fill()

def cam_profile( x_origin , y_origin , base_radius , follower_radius , scale = 1 ): #Draws cam profile
    turtle_move(x_origin + ( base_radius / scale ) , y_origin) #Moves to start point
    t.color('orange')
    t.begin_fill()
    x = [0]
    y = [0]
    for i in range(360):
        R = ( base_radius + R_list[ i ] ) #Calculates R, equation 10
        x.append(R * math.cos(math.radians( i ))) #Equation 11
        y.append(R * math.sin(math.radians( i ))) #Equation 11
    theta_total = 0
    for i in range(1, segment_no+1):
        h = displacement[i]
        beta = angular_range[i]
        for theta in range( 1 , beta + 1):
            R = ( base_radius + follower_radius + R_list[ theta_total + theta ] )
            if curve_type[i] == 1: #constant_acceleration
                    dx , dy = constant_acceleration_cam( theta , beta , i , h , R )
            elif curve_type[i] == 2: #simple_harmonic
                    dx , dy = simple_harmonic_cam( theta , beta , i , h , R )
            elif curve_type[i] == 3: #ycloidal
                    dx , dy = cycloidal_cam( theta , beta , i , h , R )
            elif motion_type[i] == 1: #Dwell
                    dx = R * math.cos(math.radians(i))
                    dy = R * math.sin(math.radians(i))
            m = math.sqrt( ( ( - dy ) ** 2 ) + ( ( dx ) ** 2 ) ) #Equation 15
            x_coord = ( x[theta_total + theta] + ( - dy / m ) ) / scale
            y_coord = ( y[theta_total + theta] + ( dx / m ) ) / scale
            turtle_draw( x_origin + x_coord , y_origin + y_coord ) #Equation 17
        theta_total += beta
    t.end_fill()

def constant_acceleration_cam( theta , beta , i , h , R ):
    if motion_type[i] == 2: #Rise
        if theta < beta / 2:
            dR = ( 4 * h * theta ) / ( beta ** 2 ) #d/dtheta equation 2
        elif theta >= beta / 2:
            dR = ( 4 * h * (1 - theta / beta ) ) / beta #d/dtheta equation 3
    if motion_type[i] == 3: #Return
        if theta < beta / 2:
            dR = - ( 4 * h * theta ) / ( beta ** 2 ) #d/dtheta equation 4
        elif theta >= beta / 2:
            dR = - ( 4 * h * (1 - theta / beta ) ) / beta #d/dtheta equation 5
    return math.cos(math.radians(theta)) * dR - R * math.sin(math.radians(theta)) , math.sin(math.radians(theta)) * dR + R * math.cos(math.radians(theta))

def simple_harmonic_cam( theta , beta , i , h , R ):
    if motion_type[i] == 2:
        dR = ( pi(1) * h ) / ( 2 * beta ) * math.sin(pi(1) * ( theta / beta ) ) #d/dtheta equation 6
    elif motion_type[i] == 3:
        dR = - ( pi(1) * h ) / ( 2* beta ) * math.sin(pi(1) * ( theta / beta ) ) #d/dtheta equation 7
    return math.cos(math.radians(theta)) * dR - R * math.sin(math.radians(theta)) , math.sin(math.radians(theta)) * dR + R * math.cos(math.radians(theta))

def cycloidal_cam( theta , beta , i , h , R ):
    if motion_type[i] == 2:
        dR = ( h / beta ) * ( 1 - math.cos( ( pi(2) * theta ) / beta ) ) #d/dtheta equation 8
    elif motion_type[i] == 3:
        dR = ( h / beta ) * ( math.cos( ( pi(2) * theta ) / beta ) - 1 ) #d/dtheta equation 9
    return math.cos(math.radians(theta)) * dR - R * math.sin(math.radians(theta)) , math.sin(math.radians(theta)) * dR + R * math.cos(math.radians(theta))

def pitch_curve( x_origin , y_origin , base_radius , follower_radius , scale = 1 ): #Draws pitch curve
    R0 = base_radius + follower_radius
    turtle_move(x_origin + ( R0 / scale ) , y_origin)
    t.color('red')
    for i in range(120): #Draws every 3 degrees, 360/3 = 120
        if i % 2 == 0: #Alternates when the line is being drawn to make it dashed
            t.pendown()
        for j in range(1,4):
            R = ( R0 + R_list[ i * 3 + j ] ) / scale #Calculates R based on scaling factor
            x = R * math.cos(math.radians(i * 3 + j)) #Equation 11
            y = R * math.sin(math.radians(i * 3 + j)) #Equation 11
            turtle_draw(x_origin + x , y_origin + y)
        t.penup()

def save_file():
    while True: #Checks whether the user wishes to save the parameters to file
        try:
            if data_choice == '2': #When the values are new
                save = int(input("Would you like to save the parameters to a file?\n1:Yes\n2:No\n"))
            elif data_choice == '1': #When the values are extracted from a file
                save = int(input("Would you like to save the parameters to another file?\n1:Yes\n2:No\n"))
            if save == 1 or save == 2: #Valid values
                return save
            else: #Invalid values
                raise ValueError("out of range")
        except ValueError as e:
            error_sorter(e)

def state():
        while True:
            try:
                state = int(input("Would you like to input another set?\n1:New set\n2:Clear screen and start new\n3:Close program\n"))
                if state == 3:
                    return False #Ends the program
                elif state == 2:
                    clearConsole() #Clears console before restarting
                    return
                elif state == 1:
                    print("\n\n") #Adds two blank lines to show start of new set
                    return
                elif state > 3 or state < 1 :
                    raise ValueError("out of range")
            except ValueError as e:
                error_sorter(e) #Returns error statement based on error

while True:
    angular_range, curve_type, motion_type, displacement = reset_var() #Resets and declares global list values.
    try:
        segment_no, base_radius, follower_radius, data_choice = data(angular_range, curve_type, motion_type, displacement) #Gets all the values of parameters needed to form displacement graph and cam follower.
        if data_check() == False: # Checks whether data can be used such as whether angle is full revolution, resets to beggining if data is invalid.
            continue
        t = turtle_setup() #Sets up turtle window and settings
        turtle.tracer(0,0) #Makes the turtle drawing very fast
        turtle_graph() #Draws displacement graph headers
        min_y, max_y, y0_position, scale_graph = min_max_checker()
        graph_axis(y_min = min_y, y_max = max_y)
        displacement_graph(yorigin = y0_position, scale = scale_graph, segment_no = segment_no ) #Draws displacement graph line using variables from data()
        drawing( 600 , 200 , base_radius , follower_radius , scale_factor() )
        turtle.update()
        turtle.tracer()
        if save_file() == 1: #Save parameters into file
            new_file( segment_no , base_radius , follower_radius )
        if state() == False:
            print("\nThe program will end now.")
            sys.exit()
        turtle.clearscreen() #Clears turtle screen when entering new set
    except ValueError as e: #Major errors to reset
        error_sorter(e)
    except IndexError:
        error_sorter("file error")
        continue
