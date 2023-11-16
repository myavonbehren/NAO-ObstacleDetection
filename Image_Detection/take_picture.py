from naoqi import ALProxy
from PIL import Image
import os
import detectBlue

IP = "192.168.4.32"
PORT = 9559

def pic(filename, CameraIndex):
    '''
    Takes a picture using NAO's camera and saves it as a PNG image.

    Args:
        filename (str): The desired name for the saved image file. If a
                        file with the same name exists, a numeric suffix
                        will be appended to avoid overwriting.
                    
        CameraIndex (int): The index of the camera to use (0 for top
                           camera, 1 for bottom camera).

    Returns:
        str: The full path to the saved image file.
    '''

    if os.path.exists(filename):
        base_name, ext = os.path.splitext(filename)
        i = 1
        while os.path.exists("%s%d%s" % (base_name, i, ext)):
            i = i + 1
        filename = "%s%d%s" % (base_name, i, ext)
    
    video = ALProxy("ALVideoDevice", IP, PORT)

    resolution = 2  
    colorSpace = 11  

    videoClient = video.subscribeCamera("python_client", CameraIndex, resolution, colorSpace, 5)

    naoImage = video.getImageRemote(videoClient)

    video.unsubscribe(videoClient)

    imageWidth = naoImage[0]
    imageHeight = naoImage[1]
    array = naoImage[6]

    im = Image.frombytes("RGB", (imageWidth, imageHeight), bytes(array))

    
    im.save(filename, "PNG")

    return filename
