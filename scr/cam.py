import cv2
import numpy as np
from time import perf_counter
from os.path import join
from random import choice

from filter import *

t = [0]

def apply_filter_glitch(img, amp = 10):
    t[0] += 10
    thr = np.random.randint(10, 50)
    n = t[0]%img.shape[0]

    p1 = n - thr
    p2 = n + thr

    dx = np.random.randint(-amp, amp)

    img[p1:p2,:,:] = np.roll(img[p1:p2,:,:], dx, axis=1)

def apply_filter_pixelate(img, n = 4):
    # n is the pixel size
    h, w, _ = img.shape
    size = (w//n, h//n)
    new_img = cv2.resize(img, size, interpolation=cv2.INTER_NEAREST)

    new_img = cv2.resize(new_img, (w, h), interpolation=cv2.INTER_NEAREST)
    return new_img

def apply_filter_blink(img):
    li = [1, 0.99, 0.98, 0.97, 0.96]
    n = choice(li)
    img[:] = img*n

def apply_filter_shadow(img):
    h, w, _ = img.shape

    mat = np.zeros(img.shape, dtype=np.uint8)

    for i in range(10):
        div = 0.5 + i*0.01
        axe = int(w*div), int(h*div)
        cv2.ellipse(mat,(w//2,h//2), axe ,0,0,360,(255,255,255),-1)
        img[mat == 0] = img[mat == 0]*0.96

def get_crt_fix(cam, p_size):
    dx = 0
    border_x = 1
    border_y = 1

    img_w = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    img_h = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

    width = (p_size - border_x - 2*dx)//3
    height = p_size - border_y

    size = img_w//p_size, img_h//p_size
    return get_crt(size, dx, border_x, border_y, width, height)
    

def main():
    p_size = 4
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    crt = get_crt_fix(cam, p_size)

    run = True
    t1 = perf_counter()
    fps = 0
    while run:
        ret, frame = cam.read()
        dt = perf_counter() - t1
        t1 = perf_counter()
        if dt:
            fps = 1/dt

        if ret:
            apply_filter_glitch(frame)
            apply_filter_blink(frame)
            apply_filter_shadow(frame)
            frame = apply_filter_pixelate(frame, p_size)

            #cv2.putText(frame, f'{fps = }', (5,50), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2)

            apply_filter(frame, crt)

            cv2.imshow('Screen', frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            run = False
        elif key == ord('s'):
            path = join('saved', 'ScreenShot.png')
            cv2.imwrite(path, frame)
            print('ScreenShot saved')

    cam.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
