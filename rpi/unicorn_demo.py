import time
import unicornhat as hat


def main():
    hat.set_layout(hat.AUTO)
    hat.rotation(180)
    hat.brightness(0.5)
    width, height=hat.get_shape()

    hat.set_pixel(7, 0, 120, 120, 0)
    hat.show()

    time.sleep(5)


if __name__ == '__main__':
    main()
