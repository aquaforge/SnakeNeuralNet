from tkinter import *
from tkinter import ttk


from PIL import Image, ImageDraw, ImageTk

# https://pillow.readthedocs.io/en/latest/reference/ImageDraw.html
# https://pycad.co/how-to-draw-on-an-image/


def drawRect(draw: ImageDraw, p: tuple, color):
    blockSize = 20
    draw.rectangle([(p[0]*blockSize+1, p[1]*blockSize+1), ((p[0]+1)*blockSize+1,
                   (p[1]+1)*blockSize+1)], fill=color, outline=(0, 0, 0), width=1)


def main():
    margin = 1
    blockSize = 20
    field = (50, 30)

    root = Tk()
    root.title(f"{field[0]}x{field[1]}")
    root.geometry("1000x800+100+100")

    frameLeft = ttk.Frame(master=root, borderwidth=1,
                          padding=10, relief=SOLID, width=300)
    frameLeft.pack(side=LEFT, fill=Y, padx=2, pady=2)
    label = ttk.Label(frameLeft, text="frameLeft")
    label.pack(anchor=NW)

    frameRight = ttk.Frame(master=root, borderwidth=1, relief=SOLID)
    frameRight.pack(fill=BOTH, expand=True,  padx=2, pady=2)

    v = ttk.Scrollbar(master=frameRight, orient=VERTICAL)
    h = ttk.Scrollbar(master=frameRight, orient=HORIZONTAL)

    canvasField = Canvas(master=frameRight, scrollregion=(0, 0, field[0]*blockSize, field[1]*blockSize),
                         bg="white", yscrollcommand=v.set, xscrollcommand=h.set)
    h["command"] = canvasField.xview
    v["command"] = canvasField.yview

    canvasField.grid(column=0, row=0, sticky=(N, W, E, S))
    h.grid(column=0, row=1, sticky=(W, E))
    v.grid(column=1, row=0, sticky=(N, S))
    frameRight.grid_columnconfigure(0, weight=1)
    frameRight.grid_rowconfigure(0, weight=1)


    img = Image.new(mode="RGB", size=(
        field[0], field[1]), color=(220, 220, 220))
    for x in range(20): 
        img.putpixel( (x, x), (0, x, 255) ) 

    img.save("a1.png")

    draw = ImageDraw.Draw(img)
    draw.line((0, 0) + img.size, fill=220)
    # PIL.Image.putpixel(xy, value)


    img = Image.new(mode="RGB", size=(
        field[0]*blockSize, field[1]*blockSize), color=(220, 220, 220))
    draw = ImageDraw.Draw(img)
    draw.line((0, 0) + img.size, fill=220)
    # draw.line((0, im.size[1], im.size[0], 0), fill=128)
    # PIL.Image.putpixel(xy, value)

    for i in range(0, 10):
        for j in range(0, 15):
            drawRect(draw, (i, j), (2*(i+j)+100, 3*(i)+100, 3*(j)+100))

    # draw.rectangle([(10, 10), (50, 50)], fill=(        255, 0, 0), outline=(0, 0, 0), width=1)


    t = ImageTk.PhotoImage(img)
    canvasField.create_image(0, 0, anchor=NW, image=t)
    '''
    for i in range(1, FIELD_HEIGHT-1):
        for j in range(1, FIELD_WIDTH-1):
            drawBlock(canvasField, (j, i),
                      fill=rgbToHTMLColor((100+i, 100+j, i+j)))
    '''
    # canvas.after(1000, start)
    root.update_idletasks()
    root.mainloop()


if __name__ == '__main__':
    main()
