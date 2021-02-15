import sys
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from utils.read_write import read_off_file
from common import MODEL_DETAILS, Models, Coords, FileDetails, Face
from model import Object
from scene import Scene



title = "3D Shapes"
DISPLAY_MATRIX = []
HEIGHT = 100
WIDTH = 100

def get_object():
   model = Models.wolf02
   model_details = MODEL_DETAILS[model]
   file_path = model_details[FileDetails.FILE_PATH]
   camera_pos = model_details[FileDetails.CAMERA_POS]
   light_source_pos = model_details[FileDetails.LIGHT_SOURCE_POS]
   camera_direction = [0, 0, -1]

    # Create model object
   obj = Object(*read_off_file(file_path).values())
   scene = Scene(camera_pos, camera_direction,
                  light_source_pos, (WIDTH, HEIGHT))
   scene.add_object(obj)
   scene.simulate_model()
   return obj 

# Initialize OpenGL Graphics
def initGL():
   glClearColor(0.0, 0.0, 0.0, 1.0) # Set background color to black and opaque
   glClearDepth(1.0)                  # Set background depth to farthest
   glEnable(GL_DEPTH_TEST)  # Enable depth testing for z-culling
   glDepthFunc(GL_LEQUAL)   # Set the type of depth-test
   glShadeModel(GL_SMOOTH)  # Enable smooth shading
   glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)  # Nice perspective corrections

 
# Handler for window-repaint event. Called back when the window first appears and
# whenever the window needs to be re-painted.
def display():
   glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Clear color and depth buffers
   glMatrixMode(GL_MODELVIEW)    # To operate on model-view matrix
   gluLookAt(0,0,0,0,0,1,0,1,0)
 
   # Render a pyramid consists of 4 triangles
   glLoadIdentity()                 # Reset the model-view matrix
   glTranslatef(-0.5, 0.0, -9.0)  # Move left and into the screen
   
   glBegin(GL_TRIANGLES)          # Begin drawing the pyramid with 4 triangles
   glColor3f(1.0, 0.0, 0.0)     # Red
   obj = get_object()
   #glBegin(GL_POLYGON)
   for i in range(obj.num_faces):
        for _,vertex_index in enumerate(obj.faces[Face.INDICES][i]):
           #print(obj.vertices[Coords.NORMALIZED][vertex_index])
           glVertex3f(
               obj.vertices[Coords.CAMERA][vertex_index][0]/70,
               obj.vertices[Coords.CAMERA][vertex_index][1]/70,
               obj.vertices[Coords.CAMERA][vertex_index][2]/70
            )
      # Right
   
   glEnd   # Done drawing the pyramid
   glColor3f(1.0, 1.0, 0.0) 
   glBegin(GL_POINTS)
   glVertex3f(60,20,10)
   glEnd
   glutSwapBuffers()  # Swap the front and back frame buffers (double buffering)

 
# Handler for window re-size event. Called back when the window first appears and
# whenever the window is re-sized with its new width and height 

def reshape(width, height):  # GLsizei for non-negative integer
   # Compute aspect ratio of the new window
   if height == 0:
        height = 1             # To prevent divide by 0
   aspect = width/height
 
   # Set the viewport to cover the new window
   glViewport(0, 0, width, height)
 
   # Set the aspect ratio of the clipping volume to match the viewport
   glMatrixMode(GL_PROJECTION)  # To operate on the Projection matrix
   glLoadIdentity()            # Reset
   # Enable perspective projection with fovy, aspect, zNear and zFar
   gluPerspective(20.0, aspect, 0.1, 50.0)
 

def main():
   glutInit(sys.argv)          # Initialize GLUT
   glutInitDisplayMode(GLUT_DOUBLE) # Enable double buffered mode
   glutInitWindowSize(1000, 800)   # Set the window's initial width & height
   glutInitWindowPosition(50, 50) # Position the window's initial top-left corner
   glutCreateWindow(title)          # Create window with the given title
   glutDisplayFunc(display)       # Register callback handler for window re-paint event
   glutReshapeFunc(reshape)      # Register callback handler for window re-size event
   initGL()                      # Our own OpenGL initialization
   glutMainLoop()                 # Enter the infinite event-processing loop

if __name__ == "__main__":
    main()