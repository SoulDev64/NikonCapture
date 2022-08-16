from ConfigurationUX import *
from gphoto2 import *

from Dashboard import Dashboard
from OpenImage import *

def get_camera():
    context = None
    camera = gp.Camera()
    try:
        camera.init()
        return camera
    except:
        return -1

root = tk.Tk()
root.title("NikonCapture # Dashboard")

# Init the camera link
camera = get_camera()

if camera != -1: # Launch only if Camera are ON and CONNECTED
    
    # Init window (aka master for the app)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(str(screen_width) + 'x' + str(screen_height))

    # Launch dashboard
    app = Dashboard(root,camera)

    # Whait while wondow are opem
    root.mainloop()

    # Release camera link
    camera.exit()

else:
    errMsg = "Error communication between camera and app. Check cable and power on"
    print(errMsg)
    showinfo(title=errMsg)
