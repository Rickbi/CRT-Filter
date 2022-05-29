import cv2
from os.path import join

from cam import *

def main():
    path = join('vid', 'test.mkv')
    path_rec = join('saved', 'test.mp4')
    vid = cv2.VideoCapture(path)
    w = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(vid.get(cv2.CAP_PROP_FPS))

    p_size = 10
    crt = get_crt_fix(vid, p_size)

    rec = cv2.VideoWriter(path_rec, cv2.VideoWriter_fourcc(*'MP4V'), fps, (w, h))
    run = True
    while run:

        ret, frame = vid.read()
        if ret:
            apply_filter_glitch(frame, 50)
            apply_filter_blink(frame)
            apply_filter_shadow(frame)
            frame = apply_filter_pixelate(frame, p_size)
            
            apply_filter(frame, crt)
            cv2.imshow('Video', frame)

            rec.write(frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            run = False
    
    vid.release()
    rec.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
    