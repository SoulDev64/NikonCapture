from ConfigurationUX import *
import gphoto2 as gp

from Dashboard import Dashboard


def get_camera():
    context = None
    camera = gp.Camera()
    camera.init()
    return camera
    '''try:
    finally:
        return False'''

# Init the camera link
camera = get_camera()

# Init window (aka master for the app)
root = tk.Tk()
root.title("AStrophoto # NikonCapture # Dashboard")
root.geometry('600x200')

if camera != False: # Launch only if Camera are ON and CONNECTED

    # Launch dashboard
    app = Dashboard(root,camera)

    # Whait while wondow are opem
    root.mainloop()

    # Release camera link
    camera.exit()

else:
    print("Error communication between camera and app. Check cable and power on")
