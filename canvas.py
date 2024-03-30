import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('QtAgg')

import sort_func as sort

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

    def setColorToZero(self, color):
        self.img[:,:,self.colors[color]] = 0
        self.setFixedImage(color)
        self.updateImage()

    def toggleColorChannels(self, color):
        if self.colorChannels[color]:
            self.fixed_img[:,:,self.colors[color]] = 0
        else:
            self.normalize(color)
        self.colorChannels[color] = not self.colorChannels[color]
        self.updateImage()

    def boxBlur3x3func(self, img):
        temp = np.copy(img)
        rows, columns = img[:,:,0].shape
        # edge corners
        img[0,0] = (temp[0,0]+temp[0,1]+temp[1,0]+temp[1,1])/4
        img[0,-1] = (temp[0,-1]+temp[0,-2]+temp[1,-1]+temp[1,-2])/4
        img[-1,0] = (temp[-1,0]+temp[-1,1]+temp[-2,0]+temp[-2,1])/4
        img[-1,-1] = (temp[-1,-1]+temp[-1,-2]+temp[-2,-1]+temp[-2,-2])/4
        # edge rows
        for j in range(1,columns-1):
            img[0,j] = (temp[0,j]+temp[0,j+1]+temp[1,j]+temp[0,j-1]+temp[1,j+1]+temp[1,j-1])/6
            img[-1,j] = (temp[-1,j]+temp[-1,j+1]+temp[-2,j]+temp[-1,j-1]+temp[-2,j+1]+temp[-2,j-1])/6
        # edge columns
        for i in range(1,rows-1):
            img[i,0] = (temp[i,0]+temp[i,1]+temp[i+1,0]+temp[i-1,0]+temp[i+1,1]+temp[i-1,1])/6
            img[i,-1] = (temp[i,-1]+temp[i,-2]+temp[i+1,-1]+temp[i-1,-1]+temp[i+1,-2]+temp[i-1,-2])/6
        #rest of the image
        for i in range(1,rows-1):
            for j in range(1,columns-1):
                img[i,j] = (temp[i,j]+temp[i,j+1]+temp[i+1,j]+temp[i,j-1]+temp[i-1,j]+temp[i+1,j+1]+temp[i-1,j-1]+temp[i+1,j-1]+temp[i-1,j+1])/9

    def boxBlur3x3(self):
        self.boxBlur3x3func(self.img)

        self.setFixedImage("r")
        self.setFixedImage("g")
        self.setFixedImage("b")
        self.updateImage()

    def sharpen(self):
        temp = np.copy(self.img)
        self.boxBlur3x3func(temp)
        self.img = 2*self.img - temp

        self.setFixedImage("r")
        self.setFixedImage("g")
        self.setFixedImage("b")
        self.updateImage()

    def sepiaTone(self):
        rows, columns = self.img[:,:,0].shape
        sepia = np.array([[0.393, 0.349, 0.272], [0.769, 0.686, 0.534], [0.189, 0.168, 0.131]])
        for i in range(rows):
            for j in range(columns):
                self.img[i][j] = np.matmul(self.img[i][j], sepia)
        
        self.setFixedImage("r")
        self.setFixedImage("g")
        self.setFixedImage("b")
        self.updateImage()

    def sortByColor(self, color):
        rows, cols, _ = self.img.shape
        self.img = self.img.reshape(rows*cols, 3)
        sort.mergeSortByColor(self.img, 0, len(self.img)-1, self.colors[color])
        self.img = self.img.reshape(rows, cols, 3)

        self.setFixedImage("r")
        self.setFixedImage("g")
        self.setFixedImage("b")
        self.updateImage()

    def sortBySum(self):
        rows, cols, _ = self.img.shape
        self.img = self.img.reshape(rows*cols, 3)
        sort.mergeSortBySum(self.img, 0, len(self.img)-1)
        self.img = self.img.reshape(rows, cols, 3)

        self.setFixedImage("r")
        self.setFixedImage("g")
        self.setFixedImage("b")
        self.updateImage()