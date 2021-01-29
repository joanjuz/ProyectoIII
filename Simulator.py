import sys
from tkinter import *
from tkinter import messagebox
import random
import os
import time
from winsound import *
from threading import Thread
import threading
import pygame
import ast
from tkinter import simpledialog
from datetime import datetime
from datetime import date



class Rectangle:
    def __init__(self ,i ,j ,canvas,color = "white", width = 0 , type = -1, size = 40, vhvariable = 0,outLcolor = "black", img = None):

        self.posi = i
        self.posj = j
        self.size = size
        self.canvas = canvas
        self.color  = color
        self.outColor = outLcolor
        self.width = width
        self.type = type
        self.imag = img
        self.vhvariable = vhvariable
        self.centerSizeRect = 2

        self.initColor()

        if self.vhvariable == 0:
            if self.imag is not None:
                self.rect = self.canvas.create_image(48*self.posi,42*self.posj, anchor = NW , image = self.imag)

            else:
                self.rect = self.canvas.create_rectangle(self.size *self.posi +self.size,self.size *self.posj + self.size
                                                         ,self.size *self.posi +2*self.size + self.width * self.size,
                                                         self.size *self.posj +2*self.size
                                                         ,fill = self.color ,outline = self.outColor)
        elif self.vhvariable == 1:

            if self.imag is not None:
                self.rect = self.canvas.create_image(48*self.posi,42*self.posj, anchor = NW , image = self.imag)
            else:
                self.rect = self.canvas.create_rectangle(self.size * self.posi + self.size,
                                                         self.size * self.posj + self.size
                                                         , self.size * self.posi + 2 * self.size ,
                                                         self.size * self.posj + 2 * self.size+ self.width * self.size
                                                         , fill=self.color, outline=self.outColor)

        if self.vhvariable == 2:

            self.rect = self.canvas.create_rectangle(self.size *self.posi +self.size + self.size/2-self.centerSizeRect,
                                                     self.size *self.posj + self.size+self.size/2-self.centerSizeRect
                                                     ,self.size *self.posi +2*self.size + self.width * self.size-self.size/2+self.centerSizeRect,
                                                     self.size *self.posj +2*self.size-self.size/2+self.centerSizeRect
                                                     ,fill = self.color ,outline = self.outColor)





        self.posx1 = self.size *self.posj
        self.posy1 = self.size *self.posi
        self.posx2 = self.size *self.posj +self.size
        self.posy2 = self.size *self.posi +self.size



    def initColor(self):
        if self.type == 0:
            self.color = "white"
        elif self.type == 1:
            self.color = "red"
        elif self.type == 2:
            self.color = "blue"
        elif self.type == 3:
            self.color = "green"
        elif self.type == 4:
            self.color = "orange"
        elif self.type == 5:
            self.color = "purple"
        elif self.type == 6:
            self.color = "yellow"


class Client():
    def __init__(self,name):

        self.window = Tk()
        self.window.resizable(False, False)
        self.window.geometry("1400x700")
        self.canvasColor = "#81948D"
        self.canvas = Canvas(self.window, width=1400, height=700, bg=self.canvasColor)
        self.canvas.place(x=0,y=0)

        self.name = name
        self.size = 40
        self.bloqueActual = 0
        self.flagJugar = False

        self.btnPlay = Button(self.canvas, text="Analizar", width=20, height=2).place(x=300,y=600)

        self.lblTitle = Label(self.window,text = "Modo Diseñador", fg = "black", bg = "white",font=("Times", 15))
        self.lblTitle.place(x = 600 ,  y = 320)

        self.lblTitle = Label(self.window, text="Modo Simulacion", fg="black", bg="white", font=("Times", 15))
        self.lblTitle.place(x=600, y=60)


        self.i = 0



        # IMAGENES


        self.imgResistorh = PhotoImage(file="Resources/resistorh.png")
        self.imgResistorv = PhotoImage(file="Resources/resistorv.png")

        self.imgSourceh = PhotoImage(file="Resources/sourceh.png")
        self.imgSourcev = PhotoImage(file="Resources/sourcev.png")




#Matriz y su tamaño


        self.matLogic = self.makeMat(10,10,0)
        self.matGraphic = self.makeMat(10,10,0)

        for i in range(len(self.matLogic[0])):
            for j in range(len(self.matLogic)):

                self.matGraphic[i][j] = Rectangle(i,j,self.canvas,self.canvasColor,outLcolor=self.canvasColor)
                r = Rectangle(i, j, self.canvas, "black",vhvariable=2)


                self.canvas.tag_bind(self.matGraphic[i][j].rect, "<ButtonPress-1>",
                                     lambda event, x=self.matGraphic[i][j].rect, id=i: self.bottonPressed(event, x, id))


        self.actualPiece = 0
        self.actualPieceInfo = ()

        self.rectanglesList = []
        self.catInMat = 0
        self.posxRadioBUttons = 605

        self.posMousex = 0
        self.posMousey = 0

        self.flagTurno = True

        self.varselection = 1

        #Prueba con imagenes

        # self.imageOption = self.canvas.create_image(250,5, anchor = NW , image = self.imgResistorh)
        # self.canvas.tag_bind(self.imageOption, "<ButtonPress-1>",
        #                      lambda event, x=self.imageOption, id=33: self.bottonPressed(event, x, id))
        # self.canvas.tag_bind(self.imageOption, "<ButtonRelease-1>",
        #                      lambda event, x=self.imageOption, id=33: self.released(event, x, id))
        # self.canvas.tag_bind(self.imageOption, "<Button1-Motion>", lambda event, id=33: self.move(event, id))


        self.rectOption5 = Rectangle(200, 5, self.canvas, type=1, width=4)
        self.rectOption6 = Rectangle(200, 7, self.canvas, type=1, width=4, vhvariable=1)

        self.rectOption7 = Rectangle(200, 5, self.canvas, type=1, width=4)
        self.rectOption8 = Rectangle(200, 7, self.canvas, type=1, width=4, vhvariable=1)



        self.canvas.tag_bind(self.rectOption5.rect, "<ButtonPress-1>", lambda event, x= self.rectOption5.rect, id = 5: self.bottonPressed(event, x, id))
        self.canvas.tag_bind(self.rectOption5.rect, "<ButtonRelease-1>",lambda event, x=self.rectOption5, id = 5: self.released(event, x,id))
        self.canvas.tag_bind(self.rectOption5.rect, "<Button1-Motion>", lambda event, id = 5: self.move(event,id))

        self.canvas.tag_bind(self.rectOption6.rect, "<ButtonPress-1>", lambda event, x= self.rectOption6.rect, id = 6: self.bottonPressed(event, x, id))
        self.canvas.tag_bind(self.rectOption6.rect, "<ButtonRelease-1>",lambda event, x=self.rectOption6, id = 6: self.released(event, x,id))
        self.canvas.tag_bind(self.rectOption6.rect, "<Button1-Motion>", lambda event, id = 6: self.move(event,id))


        self.typeRectangle = IntVar(value = 1)


        self.lblContNav3 = Label(self.canvas, text="Disponibles:")
        self.lblContNav3.place(x=self.posxRadioBUttons-40, y=self.size * 8+60)

        self.btncategory3 = Radiobutton(self.window,
                       text="Resistor",
                       padx=20,
                       variable=self.typeRectangle,
                       value=3,command = (lambda x=1:self.intermed(x)), bg = "white")
        self.btncategory3.place(x=self.posxRadioBUttons+40, y=self.size * 8+60)

        self.lblContNav4 = Label(self.canvas, text="Disponibles:")
        self.lblContNav4.place(x=self.posxRadioBUttons-40, y=self.size * 8+90)

        self.btncategory4 = Radiobutton(self.window,
                       text="Source",
                       padx=20,
                       variable=self.typeRectangle,
                       value=4,command = (lambda x=2:self.intermed(x)), bg = "white")
        self.btncategory4.place(x=self.posxRadioBUttons+40, y=self.size * 8+90)

        self.btncategory5 = Radiobutton(self.window,
                                        text= "Simulate",
                                        padx=20,
                                        variable=self.typeRectangle,
                                        value=5,command = (lambda x=3:self.intermed(x)),bg="white")
        self.btncategory5.place(x=self.posxRadioBUttons+10,y=self.size * 4)

        self.btncategory6 = Radiobutton(self.window,
                                        text="Reset Num",
                                        padx=20,
                                        variable=self.typeRectangle,
                                        value=6, command=(lambda x=4: self.intermed(x)), bg="white")
        self.btncategory6.place(x=self.posxRadioBUttons + 10, y=self.size * 4 + 40)




        self.flagConv = False

        #self.printRectangleTYPE(self.varselection)

        self.window.bind("<Motion>",self.updateMousexy)


        self.window.mainloop()

    def reiniciar(self):
        self.window.destroy()
        ng = Client(self.name)


    def isEmpty(self,matrix):
        for i in matrix:
            for j in i:
                if j != 0:
                    return False
        return True

    def exist(self,number):
        for i in self.matLogic:
            if number in i:
                return True
        return False

    def getCount(self,number):
        cont = 0
        for i in self.matLogic:
            cont += i.count(number)
        return cont


    def updateMousexy(self,event):
        self.posMousex = event.x//self.size
        self.posMousey = event.y//self.size

    def intermed(self,x):
        self.printRectangleTYPE(x)

    def printRectangleTYPE(self,vsel):
        self.varselection = vsel


        self.canvas.delete(self.rectOption5.rect)
        self.canvas.delete(self.rectOption6.rect)
        self.canvas.delete(self.rectOption7.rect)
        self.canvas.delete(self.rectOption8.rect)




        if self.varselection == 1:


            self.rectOption5 = Rectangle(24, 5, self.canvas, type=3, width=2,img=self.imgResistorh)
            self.rectOption6 = Rectangle(24, 7, self.canvas, type=3, width=2, vhvariable=1, img = self.imgResistorv)

            self.canvas.tag_bind(self.rectOption5.rect, "<ButtonPress-1>",
                                 lambda event, x=self.rectOption5.rect, id=5: self.bottonPressed(event, x, id))
            self.canvas.tag_bind(self.rectOption5.rect, "<ButtonRelease-1>",
                                 lambda event, x=self.rectOption5, id=5: self.released(event, x, id))
            self.canvas.tag_bind(self.rectOption5.rect, "<Button1-Motion>", lambda event, id=5: self.move(event, id))

            self.canvas.tag_bind(self.rectOption6.rect, "<ButtonPress-1>",
                                 lambda event, x=self.rectOption6.rect, id=6: self.bottonPressed(event, x, id))
            self.canvas.tag_bind(self.rectOption6.rect, "<ButtonRelease-1>",
                                 lambda event, x=self.rectOption6, id=6: self.released(event, x, id))
            self.canvas.tag_bind(self.rectOption6.rect, "<Button1-Motion>", lambda event, id=6: self.move(event, id))


        elif self.varselection == 2:
            self.rectOption7 = Rectangle(24, 5, self.canvas, type=4, width=2,img=self.imgSourceh)
            self.rectOption8 = Rectangle(24, 7, self.canvas, type=4, width=2, vhvariable=1,img = self.imgSourcev)

            self.canvas.tag_bind(self.rectOption7.rect, "<ButtonPress-1>",
                                 lambda event, x=self.rectOption7.rect, id=7: self.bottonPressed(event, x, id))
            self.canvas.tag_bind(self.rectOption7.rect, "<ButtonRelease-1>",
                                 lambda event, x=self.rectOption7, id=7: self.released(event, x, id))
            self.canvas.tag_bind(self.rectOption7.rect, "<Button1-Motion>", lambda event, id=7: self.move(event, id))

            self.canvas.tag_bind(self.rectOption8.rect, "<ButtonPress-1>",
                                 lambda event, x=self.rectOption8.rect, id=8: self.bottonPressed(event, x, id))
            self.canvas.tag_bind(self.rectOption8.rect, "<ButtonRelease-1>",
                                 lambda event, x=self.rectOption8, id=8: self.released(event, x, id))
            self.canvas.tag_bind(self.rectOption8.rect, "<Button1-Motion>", lambda event, id=8: self.move(event, id))
        elif self.varselection == 3:
            print("Simulacion")
        elif self.varselection == 4:
            self.i = 0


    def SALIR(self):
        self.window.destroy()
        MenuG()


    def makeMat(self,f,c,val):
        mat = []
        for i in range(f):
            lista = []
            for j in range(c):
                lista += [val]
            mat += [lista]
        return mat

    def findRectangle(self,number):
        for row in self.matG:
            for rect in row:
                if rect.realPosition == number:
                    return rect
        return number

    def released(self,event,object,id):
        if not self.varselection == 3:
            if self.posMousex >= 1 and self.posMousex <= 10 and self.posMousey>= 1 and self.posMousey <= 10:

                if 1:

                    if self.flagConv:
                        messagebox.showinfo("Error",
                                            message="")
                        self.printRectangleTYPE(self.varselection)
                    else:

                        r = None



                        if id == 5:
                            if self.posMousex > 8:
                                self.posMousex -= (2 + (self.posMousex - 10))
                            r = Rectangle(self.posMousex - 1, self.posMousey - 1, self.canvas, type=object.type, width=2,img=self.imgResistorh)

                            self.matLogic[self.posMousey - 1][self.posMousex - 1] = object.type
                            self.matLogic[self.posMousey - 1][self.posMousex] = object.type
                            self.matLogic[self.posMousey - 1][self.posMousex + 1] = object.type


                            self.lblContNav3.config(text="Disponibles:")


                        elif id == 6 :
                            if self.posMousey > 8:
                                self.posMousey -= (2 + (self.posMousey - 10))
                            r = Rectangle(self.posMousex - 1, self.posMousey - 1, self.canvas, type=object.type, width=2,
                                          vhvariable=1, img = self.imgResistorv)
                            self.matLogic[self.posMousey - 1][self.posMousex - 1] = object.type
                            self.matLogic[self.posMousey][self.posMousex - 1] = object.type
                            self.matLogic[self.posMousey + 1][self.posMousex - 1] = object.type


                            self.lblContNav3.config(text="Disponibles:")


                        elif id == 7:
                            if self.posMousex > 9:
                                self.posMousex -= (1 + (self.posMousex - 10))
                            r = Rectangle(self.posMousex - 1, self.posMousey - 1, self.canvas, type=object.type, width=2,img = self.imgSourceh)

                            self.matLogic[self.posMousey - 1][self.posMousex - 1] = object.type
                            self.matLogic[self.posMousey - 1][self.posMousex] = object.type


                            self.lblContNav4.config(text="Disponibles:")



                        elif id == 8:
                            if self.posMousey > 9:
                                self.posMousey -= (1 + (self.posMousey - 10))
                            r = Rectangle(self.posMousex - 1, self.posMousey - 1, self.canvas, type=object.type, width=2,
                                          vhvariable=1,img = self.imgSourcev)
                            self.matLogic[self.posMousey - 1][self.posMousex - 1] = object.type
                            self.matLogic[self.posMousey][self.posMousex - 1] = object.type


                            self.lblContNav4.config(text="Disponibles:")





                        if r!=None:
                            self.canvas.tag_bind(r.rect, "<ButtonPress-1>",
                                                 lambda event, x=r.rect, id=id: self.bottonPressed(event, x, id))
                            self.canvas.tag_bind(r.rect, "<ButtonRelease-1>",
                                                 lambda event, x=r, id=id: self.released(event, x, id))
                            self.canvas.tag_bind(r.rect, "<Button1-Motion>",
                                                 lambda event, id=id: self.move(event, id))

                            self.rectanglesList += [r]


                        self.printRectangleTYPE(self.varselection)



                self.printM(self.matLogic,"Matriz Actual")


            else:
                if self.categoryInMatrix(object.type) and self.categoryInListRectangles(object.type):

                    self.deleteCategoryMatriz(object.type)



                self.printRectangleTYPE(self.varselection)
        else:
            print("Simulation",self.i)
            if self.posMousex >= 1 and self.posMousex <= 10 and self.posMousey >= 1 and self.posMousey <= 10:
                if id == 5:
                    if self.posMousex > 8:
                        self.posMousex -= (2 + (self.posMousex - 10))
                elif id == 6:
                    if self.posMousey > 8:
                        self.posMousey -= (2 + (self.posMousey - 10))
                elif id == 7:
                    if self.posMousex > 9:
                        self.posMousex -= (1 + (self.posMousex - 10))
                elif id == 8:
                    if self.posMousey > 9:
                        self.posMousey -= (1 + (self.posMousey - 10))
                print("x:"+ str(self.posMousex),"y:" + str(self.posMousey))
                Label(self.canvas,text=str(self.i)+" Ω").place(x=(self.posMousex*50)-60, y=(self.posMousey - 1)*50)
                self.i += 1


    def bottonPressed(self,event, x,id):
        if not self.varselection == 3:
            self.actualPiece = x
            self.actualPieceInfo = (self.actualPiece, event.x, event.y)
        print(self.posMousex,self.posMousey)

    def move(self,event,id):
        self.canvas.move(self.actualPieceInfo[0], event.x - self.actualPieceInfo[1],
                             event.y - self.actualPieceInfo[2])
        self.actualPieceInfo = (self.actualPiece, event.x, event.y)

    def categoryInMatrix(self,type):
        for i in self.matLogic:
            for j in i:
                if j == type:
                    return True
        return False

    def categoryInListRectangles(self,t):
        for i in self.rectanglesList:
            if i.type == t:
                return True
        return False

    def deleteCategoryMatriz(self,c):
        for i in range(len(self.matLogic)):
            for j in range(len(self.matLogic[0])):
                if self.matLogic[i][j] == c:

                    self.matLogic[i][j] = 0
                    for k in range(len(self.rectanglesList)):
                        if self.rectanglesList[k].posj == i and self.rectanglesList[k].posi == j:
                            self.canvas.delete(self.rectanglesList[k].rect)
                            self.rectanglesList.remove(self.rectanglesList[k])
                            break
        if c != 6:
            self.catInMat -= 1

    def printM(self,matriz,message = ""):
        print(message)
        for i in matriz:
            print(i)

class MenuG:
    def __init__(self):

        # window
        self.window = Tk()
        self.window.geometry("450x250+300+200")
        self.window.title("Bienvenido a Simulator! ")
        self.window.minsize(500, 250)
        self.window.resizable(width="NO", height="NO")


        # buttons

        self.canvas = Canvas(self.window,width= 500 ,height=250 ,bg= "black")
        self.canvas.place(x = 0, y = 0)
        self.rect1 = self.canvas.create_rectangle(0,0,500,250,fill = "blue")
        self.text1 = self.canvas.create_text(240,125,fill = "black", text = "Comenzar")
        self.canvas.tag_bind(self.rect1, "<ButtonPress-1>",lambda event,  id = 1 : self.pressed(event,id))




        self.window.bind("<Motion>",self.effect)


        self.window.mainloop()

    def effect(self,event):

        i = event.x//250

        if i == 0 :
            self.rect1  = self.canvas.create_rectangle(0,0,500,250,fill = "blue")
            self.canvas.tag_bind(self.rect1, "<ButtonPress-1>", lambda event, id=1: self.pressed(event, id))

        elif i == 1:

            self.rect1 = self.canvas.create_rectangle(0, 0, 500, 250, fill="#7E9AF7")
            self.canvas.tag_bind(self.rect1, "<ButtonPress-1>", lambda event, id=1: self.pressed(event, id))
        else:
            self.rect1  = self.canvas.create_rectangle(0, 0, 500, 250, fill="blue")
            self.canvas.tag_bind(self.rect1, "<ButtonPress-1>", lambda event, id=1: self.pressed(event, id))

        self.text1 = self.canvas.create_text(240, 125, fill="black", text="Comenzar")

    def pressed(self,event,id):

        if id == 1:
            #answer = simpledialog.askstring("Input", "Ingresa tu nombre?",
             #                               parent=self.window)
            #if answer is not None:
            self.window.destroy()
            Client("Simulator")

m = MenuG()