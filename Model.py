'''Needed Points:
Validation of input received by your application (Have any non-intuitive input display something to say it worked)
Exception handling to deal with errors (Iff there is any risk of errors)
An intuitive GUI for your application (you are free to use any GUI framework).
Code organized with the help of classes or modules
Data stored in files/databases (Only for projects that acutally store data)
Proper code documentation (descriptive variable names, docstrings for functions/methods, use of type hinting, and descriptive commit messages)'''

import pygame
import math

#Width and Height of the window
wWidth = 800
wHeight = 800

#Initalize x, y, z values of each vertex
    #  0 ,  1 ,  2 ,  3 ,  4 ,  5 ,  6 ,  7
x = [-200, 200,-200, 200,-200, 200,-200, 200]
y = [-200,-200, 200, 200,-200,-200, 200, 200]
z = [-200,-200,-200,-200, 200, 200, 200, 200]

#Create array of arrays, which each contain the ordered points of each face
f = [[0, 1, 3, 2], #0
     [0, 1, 5, 4], #1
     [0, 2, 6, 4], #2
     [1, 3, 7, 5], #3
     [2, 3, 7, 6], #4
     [4, 5, 7, 6]] #5

def main():
   #Create the window with initialized width and height, and title it
   pygame.init()
   screen = pygame.display.set_mode([wWidth, wHeight])
   pygame.display.set_caption("3D Model")

   #Start the program and allow it to be destroyed when the 'X' box is clicked
   done = False
   clock = pygame.time.Clock()
   while not done:
      clock.tick(50) #Frames per second
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            done = True
      
      #Draw the white background
      screen.fill((127, 127, 127))

      numVerts = len(x) #Number of verticies

      #Transform the normal positions into their drawn positions for each point
      xDraw = [0, 0, 0, 0, 0, 0, 0, 0]
      yDraw = [0, 0, 0, 0, 0, 0, 0, 0]
      for p in range(numVerts):
         (xDraw[p],yDraw[p]) = perspective(x[p],y[p],z[p])
      
      #Sort the faces to draw them in order, so that further faces are hidden behind closer ones
      numFaces = len(f)
      #zArr = [0, 0, 0, 0, 0, 0]#, 0, 0]
      zArr = list(range(numFaces))
      for face in range(numFaces): #Create a pair of lists (sort of) with one containing the Z positions of each face and the second a set of incrementing IDs
         #Average the Z positions of each point of a face
         zAvg = 0
         for point in range(len(f[face])):
            zAvg += z[f[face][point]]/4
         zArr[face] = [zAvg, face]
      zArr = sorted(zArr, key=lambda e: e[0]) #Sort the first list, with the IDs of the second being reordered along with them
      
      #Draw the faces, each being a polygon with points ordered in the f matrix, and colours ordered in the colors array
      colors = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (255,0,255), (0,255,255), (255,255,255), (0, 0, 0)]
      for face in range(numFaces):
         n = int(zArr[face][1])
         points = list(range(len(f[face])))
         for point in range(len(f[face])):
            points[point] = [xDraw[f[n][point]],yDraw[f[n][point]]]
         pygame.draw.polygon(screen, colors[n], points)

      #Take inputs and allow for printing the currently processed inputs
      keys = pygame.key.get_pressed()
      end = ""
      #Rotate around an axis or multiple axes, with opposite directions incompatible. (Math is done using linear algebra)
      if keys[pygame.K_w]: #Rotate clockwise around X-axis
         end += "W"
         for p in range(numVerts):
            zp = z[p]
            yp = y[p]
            z[p] = math.cos(-.03)*zp + math.sin(-.03)*yp
            y[p] = math.cos(-.03)*yp - math.sin(-.03)*zp
      elif keys[pygame.K_s]: #Rotate counterclockwise around X-axis
         end += "S"
         for p in range(numVerts):
            zp = z[p]
            yp = y[p]
            z[p] = math.cos(.03)*zp + math.sin(.03)*yp
            y[p] = math.cos(.03)*yp - math.sin(.03)*zp
      if keys[pygame.K_a]: #Rotate clockwise around Y-axis
         end += "A"
         for p in range(numVerts):
            xp = x[p]
            zp = z[p]
            x[p] = math.cos(.03)*xp + math.sin(.03)*zp
            z[p] = math.cos(.03)*zp - math.sin(.03)*xp
      elif keys[pygame.K_d]: #Rotate counterclockwise around Y-axis
         end += "D"
         for p in range(numVerts):
            xp = x[p]
            zp = z[p]
            x[p] = math.cos(-.03)*xp + math.sin(-.03)*zp
            z[p] = math.cos(-.03)*zp - math.sin(-.03)*xp
      if keys[pygame.K_e]: #Rotate clockwise around Z-axis
         end += "A"
         for p in range(numVerts):
            xp = x[p]
            yp = y[p]
            x[p] = math.cos(-.03)*xp + math.sin(-.03)*yp
            y[p] = math.cos(-.03)*yp - math.sin(-.03)*xp
      elif keys[pygame.K_q]: #Rotate counterclockwise around Z-axis
         end += "D"
         for p in range(numVerts):
            xp = x[p]
            yp = y[p]
            x[p] = math.cos(.03)*xp + math.sin(.03)*yp
            y[p] = math.cos(.03)*yp - math.sin(.03)*xp
      #Reset the positions of different models by pressing the cooresponding key
      if keys[pygame.K_c]: #Reset positions for Cube
         end += "C"
         cube()
      elif keys[pygame.K_o]: #Reset positions for Octohedron
         end += "O"
         octo()
      elif keys[pygame.K_t]: #Reset positions for Tetrahedron
         end += "T"
         tetra()
      #Print the processed inputs for that frame, or a blank line if nothing is pressed
      #print(end)

      #Finish the drawing for this frame
      pygame.display.flip()    
      
   #Quite the execution when clicking on close    
   pygame.quit()



#Apply perspective to and reposition the input point, creating a 2D point to draw in the window. Done for every point on every frame.
def perspective(xIn, yIn, zIn):
   xOut = xIn * math.pow(2, zIn/400) + wWidth/2
   yOut = yIn * math.pow(2, zIn/400) + wHeight/2
   return (xOut, yOut)


#Reset methods reset the lists of x,y,z coordinates to move each point back into the default place, 
# with list of lists f also being reset to reassign the faces to the new model's points in case the model is being changed

#Reset positional variables for Cube
def cube():
   global x,y,z,f
       #  0 ,  1 ,  2 ,  3 ,  4 ,  5 ,  6 ,  7
   x = [-200, 200,-200, 200,-200, 200,-200, 200]
   y = [-200,-200, 200, 200,-200,-200, 200, 200]
   z = [-200,-200,-200,-200, 200, 200, 200, 200]
   f = [[0, 1, 3, 2], #0
        [0, 1, 5, 4], #1
        [0, 2, 6, 4], #2
        [1, 3, 7, 5], #3
        [2, 3, 7, 6], #4
        [4, 5, 7, 6]] #5

#Reset positional variables for Octohedron
def octo():
   global x,y,z,f
   x = [-200,  200,    0,    0,    0,    0]
   y = [   0,    0, -200,  200,    0,    0]
   z = [   0,    0,    0,    0, -200,  200]
   f = [[0, 2, 4],
        [0, 2, 5],
        [0, 3, 4],
        [0, 3, 5],
        [1, 2, 4],
        [1, 2, 5],
        [1, 3, 4],
        [1, 3, 5]];

#Reset positional variables for Tetrahedron
def tetra():
   global x,y,z,f
   x = [   -200,     200,      0,       0];
   y = [ 115.47,  115.47, 115.47, -230.95];
   z = [-115.47, -115.47, 230.95,       0];
   f = [[0, 1, 3],
        [0, 2, 3],
        [1, 2, 3],
        [0, 1, 2]];


if __name__ == '__main__':
   main()