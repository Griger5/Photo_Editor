import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('QtAgg')

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, file, parent=None, width=1, height=1, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig.clear()
        self.axes = self.fig.add_subplot(111)
        self.axes.clear()
        self.axes.axis("off")
        self.axes.margins(x=0, y=0)
        self.fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

        self.img = plt.imread(file)
        self.img = np.asarray(self.img)
        if file.lower().endswith(".png"):
            self.img = (self.img[:,:,[0,1,2]]*255).astype(int)
            self.axes.imshow(self.img)
        elif file.lower().endswith((".jpg", ".jpeg", ".webp")):
            self.img = self.img.astype(int)
            self.axes.imshow(self.img)

        # necessary to keep the differences in color values between pixels intact
        self.fixed_img = np.copy(self.img)

        self.colors = {"r":0, "g":1, "b":2}
        self.addColorReverse = {"r":False, "g":False, "b":False}
        self.colorChannels = {"r":True, "g":True, "b":True}

        plt.draw()
        super().__init__(self.fig)

    def saveImage(self, filename):
        if filename.lower().endswith((".jpg", ".jpeg", ".webp", ".png")):
            plt.imsave(filename, self.fixed_img.astype(np.uint8))
        elif filename:
            plt.imsave(filename+".png", self.fixed_img.astype(np.uint8))
        else:
            ...

    def updateImage(self):
        self.axes.clear()
        self.axes.axis('off')
        self.axes.imshow(self.fixed_img)
        self.draw()

    def normalize(self, color):
        rows = self.img[:,0,0].shape[0]
        for i in range(rows):
            self.fixed_img[:,:,self.colors[color]][i] = np.array([255 if x>255 else 0 if x<0 else x for x in self.img[:,:,self.colors[color]][i]])

    def setFixedImage(self, color):
        if self.colorChannels[color]:
            self.normalize(color)
        else:
            self.fixed_img[:,:,self.colors[color]] = 0

    def addColor(self, color, multiplier):
        multiplier = -multiplier if self.addColorReverse[color] else multiplier
        self.img[:,:,self.colors[color]] = self.img[:,:,self.colors[color]]+np.ones(self.img[:,:,0].shape)*multiplier
        self.setFixedImage(color)
        self.updateImage()
    def reverseAddColor(self, color):
        self.addColorReverse[color] = not self.addColorReverse[color]

    def toggleColorChannels(self, color):
        if self.colorChannels[color]:
            self.fixed_img[:,:,self.colors[color]] = 0
        else:
            self.normalize(color)
        self.colorChannels[color] = not self.colorChannels[color]
        self.updateImage()