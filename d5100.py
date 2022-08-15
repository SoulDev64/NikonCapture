from ConfigurationUX import *
import gphoto2 as gp

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
    root.geometry('600x200')

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
