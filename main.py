import os
import pyautogui
import time
from PIL import Image
import winsound
import shutil

frequency = 1000  # 1000 Hz
duration = 500    # 1000 ms
temp_directory = "tempimages"
filename = 'exported' + '.pdf'

def make_screenshots(num_screenshots, directory, x1, y1, x2, y2):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory '{directory}' created.")

    print("Go to the application. Taking screenshots in 10 seconds...")    
    time.sleep(10)

    image_files = []
    my_region =(x1, y1, x2-x1, y2-y1)
    for i in range(num_screenshots):
        screenshot = pyautogui.screenshot(region=my_region)
        source_path = os.path.join(directory, f'{i + 1}.png')
        screenshot.save(source_path)
        image_files.append(source_path)

        pyautogui.press('left')
        # waiting for application to render page
        time.sleep(1)

    return image_files

def export_pdf(image_files, filename):    

    if not image_files:
        print("No source image!")
        return

    images = [Image.open(img).convert('RGB') for img in image_files]
    images[0].save(filename, save_all=True, append_images=images[1:])
    print(f"Exported: {filename}")

    # cleanup:
    for img_file in image_files:
        os.remove(img_file)
    

def take_screen_addresses():
    x1=x2=y1=y2=0
    print ("Move your pointer to the top-left of the interested area and wait until you hear a beep.")
    time.sleep(10)
    x1,y1=pyautogui.position()        
    winsound.Beep(frequency, duration)

    print ("Move your pointer to the end-right of the interested are and wait until you hear two beeps.")
    time.sleep(10)
    x2,y2=pyautogui.position()
    winsound.Beep(frequency, duration)
    time.sleep(0.2)
    winsound.Beep(frequency, duration)
    print (x2,", ", y2)
    return x1,y1,x2,y2
   
    
def main():
   
    while True:
        try:
            page_numbers = int(input("how many pages you want to export? "))
            if page_numbers > 0 : 
                break
            else:
                print("Enter a valid number please!")
        except ValueError:
            print("Enter a valid number please!")


    while True:
        x1,y1,x2,y2 =take_screen_addresses()
        print("The selected area is: " , x1 ,",", y1 ," to " ,x2,"," ,y2 )
        accepted = input( "Is it accepted? (y/n)")
        if accepted == "y":
            break
    
    imagefiles =make_screenshots(page_numbers, temp_directory, x1, y1, x2, y2)
    export_pdf(imagefiles, filename)
    shutil.rmtree(temp_directory)
    input("Press enter key to close this window")

if __name__ == "__main__":
    main()
