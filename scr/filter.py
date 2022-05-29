import numpy as np
import cv2
from os.path import join

def load(name, ext = 'png'):
    path = join('img', f'{name}.{ext}')
    return cv2.imread(path)


def save(name, img, ext = 'png'):
    path = join('saved', f'{name}.{ext}')
    cv2.imwrite(path, img)
    print(f'Image Saved as {name}')


def show(img):
    run = True
    while run:
        cv2.imshow('Screen', img)
        key = cv2.waitKey(1)
        if key == ord('q'):
            run = False
    cv2.destroyAllWindows()


def draw_rect(screen, pos, size, color):
    pos2 = pos[0] + size[0] - 1, pos[1] + size[1] - 1
    cv2.rectangle(screen, pos, pos2, color, -1)


def draw_pixel(screen, pos, size, dx):
    pg = pos[0] + size[0] + dx, pos[1]
    pb = pos[0] + 2*size[0] + 2*dx, pos[1]
    draw_rect(screen, pos, size, (0,0,255))
    draw_rect(screen, pg, size, (0,255,0))
    draw_rect(screen, pb, size, (255,0,0))


def get_crt(size, dx = 1, border_x = 1, border_y = 1, width = 3, height = 11):
    px, py = width*3 + dx*2 + border_x, height + border_y
    w, h = px*size[0], py*size[1]
    screen = np.zeros((h,w,3), dtype=np.uint8)

    for x in range(size[0]):
        for y in range(size[1]):
            pos = (px*x, py*y)
            draw_pixel(screen, pos, (width, height), dx)
    return screen


def filter_tem(img, crt, color):
    img_c = img[:,:,color]
    crt_c = crt[:,:,color]

    img_c[crt_c != 255] = 1


def apply_filter(img, crt):
    filter_tem(img, crt, 0)
    filter_tem(img, crt, 1)
    filter_tem(img, crt, 2)


def apply_filter_per_pixel(img_name):
    dx = 0
    border_x = 1
    border_y = 1
    width = 5
    height = 15

    img = load(img_name)
    img_h, img_w, _ = img.shape
    save(f'{img_name}_org', img)

    crt = get_crt((img_w, img_h), dx, border_x, border_y, width, height)
    crt_h, crt_w, _ = crt.shape

    res = cv2.resize(img, (crt_w, crt_h), interpolation=cv2.INTER_NEAREST)
    save(f'{img_name}_big', res)

    apply_filter(res, crt)
    save(f'{img_name}_crt', res)


def apply_filter_per_block_tem(img_name, p_size):
    dx = 0
    border_x = 1
    border_y = 1

    n = (p_size-1)//3
    p = n*3 + 1

    img = load(img_name)
    img_h, img_w, _ = img.shape

    size = img_w//p_size, img_h//p_size
    img_w, img_h = size[0]*p, size[1]*p

    img = cv2.resize(img, (img_w, img_h), interpolation=cv2.INTER_NEAREST)
    save(f'{img_name}_org', img)

    width = (p - border_x - 2*dx)//3
    height = p - border_y

    crt = get_crt(size, dx, border_x, border_y, width, height)

    apply_filter(img, crt)
    save(f'{img_name}_crt', img)


def apply_filter_per_block(img_name, p_size):
    dx = 0
    border_x = 1
    border_y = 1

    img = load(img_name)
    img_h, img_w, _ = img.shape
    save(f'{img_name}_org', img)

    width = (p_size - border_x - 2*dx)//3
    height = p_size - border_y

    size = img_w//p_size, img_h//p_size
    crt = get_crt(size, dx, border_x, border_y, width, height)

    apply_filter(img, crt)
    save(f'{img_name}_crt', img)

def main():
    #apply_filter_per_pixel('test1')
    apply_filter_per_block_tem('test', 12)
    #apply_filter_per_block('test6', 6)



if __name__ == '__main__':
    main()
