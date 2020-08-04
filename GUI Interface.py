from tkinter import *
import numpy as np
from scipy.integrate import odeint
		
root = Tk() 
root.title("CRYPTOGRAPHY") 
root.geometry("800x600") 


# creating labels and positioning them on the grid 
l1 = Label(root, text ="Enter parameter 1 (type float and > 0)")			 
l1.grid(row = 10, column = 1) 
l2 = Label(root, text ="Enter parameter 2 (type float and > 0)") 
l2.grid(row = 11, column = 1) 
l3 = Label(root, text ="Enter parameter 3 (type float and > 0)") 
l3.grid(row = 12, column = 1) 
l4 = Label(root, text ="Enter parameter 4 (type float and > 0)") 
l4.grid(row = 13, column = 1)     
l5 = Label(root, text ="Enter parameter 5 (type float and > 0)")
l5.grid(row = 14, column = 1) 
l6 = Label(root, text ="Enter parameter 6 (type float and > 0)") 
l6.grid(row = 15, column = 1) 
l7 = Label(root, text ="Enter length of the key (type int and > 0)") 
l7.grid(row = 16, column = 1)  

l8 = Label(root, text ='Plain text')
l8.grid(row = 70, column = 1) 
l9 = Label(root, text ='Encrypted text') 
l9.grid(row = 71, column = 1) 
l10 = Label(root, text ="Cipher text") 
l10.grid(row = 70, column = 10) 
l11 = Label(root, text ="Decrypted text") 
l11.grid(row = 71, column = 10) 

# creating entries and positioning them on the grid 
e1 = Entry(root) 
e1.grid(row = 10, column = 2) 
e2 = Entry(root) 
e2.grid(row = 11, column = 2) 
e3 = Entry(root) 
e3.grid(row = 12, column = 2) 
e4 = Entry(root) 
e4.grid(row = 13, column = 2) 
e5 = Entry(root) 
e5.grid(row = 14, column = 2) 
e6 = Entry(root) 
e6.grid(row = 15, column = 2) 
e7 = Entry(root) 
e7.grid(row = 16, column = 2) 
e8 = Entry(root) 
e8.grid(row = 70, column = 2) 
e9 = Entry(root) 
e9.grid(row = 71, column = 2) 
e10 = Entry(root) 
e10.grid(row = 70, column = 15) 
e11 = Entry(root) 
e11.grid(row = 71, column = 15) 




def derivative(y, t, L1, L2, m1, m2):
    alpha, z1, beta, z2 = y
    c, s = np.cos(alpha-beta), np.sin(alpha-beta)
    dalpha = z1
    dz1 = (m2*9.81*np.sin(beta)*c - m2*s*(L1*z1**2*c + L2*z2**2) - (m1+m2)*9.81*np.sin(alpha)) / L1 / (m1 + m2*s**2)
    dbeta = z2
    dz2 = ((m1+m2)*(L1*z1**2*s - 9.81*np.sin(beta) + 9.81*np.sin(alpha)*c) + m2*L2*z2**2*s*c) / L2 / (m1 + m2*s**2)
    return dalpha, dz1, dbeta, dz2

def key():
    tmax = (float(e7.get()))*0.1
    dt = 0.01
    t = np.arange(0, tmax+dt, dt)
    y0 = np.array([float(e5.get())*np.pi/180, 0, float(e6.get())*np.pi/180, 0])
    y = odeint(derivative, y0, t, args=(float(e1.get()), float(e2.get()), float(e3.get()), float(e4.get())))
    alpha, beta = y[:,0], y[:,2]
    x1, y1 = float(e1.get()) * np.sin(alpha), -float(e1.get()) * np.cos(alpha)
    x2, y2 = x1 + float(e2.get()) * np.sin(beta), y1 - float(e2.get()) * np.cos(beta)
    fps = 10
    di = int(1/fps/dt)
    alphabets = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    Key = ''
    for i in range(0, t.size, di):
        key = alphabets[int(str(x2[i] + y2[i])[8:11])%26]
        Key += key
    #print(Key)
    return str(Key)

def charToNum(char):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    num = 0
    for letter in alphabet:
        if letter == char:
            break
        else:
            num+=1
    return num

def encodeChar(pText, key):
    cNum = ( charToNum(pText) + charToNum(key) ) % 26
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    cText = alphabet[cNum]
    return cText

def decodeChar(cText, key):
    pNum = (charToNum(cText) - charToNum(key))%26
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    pText = alphabet[pNum]
    return pText


def encode(pText, key):
    cText= ""
    for i in range(0, len(pText)):
        cText += encodeChar(pText[i], key[i])
    return cText

def decode(cText, key):
    pText=""
    for i in range(0, len(cText)):
        pText += decodeChar(cText[i], key[i])
    return pText

def encryptMessage():					 
	pt = str(e8.get())
	ct = str(encode(pt, key()))
	e9.insert(0, ct)

def decryptMessage():					 
	ct1 = str(e10.get())
	pt1 = str(decode(ct1, key()))
	e11.insert(0, pt1) 
	

# creating encryption button to produce the output 
b1 = Button(root, text = "Generate Key", bg ="Blue", fg ="white", command = key) 
b1.grid(row = 17, column = 2)

b2 = Button(root, text = "ENCRYPT", bg ="red", fg ="white", command = encryptMessage) 
b2.grid(row = 73, column = 2) 

# creating decryption button to produce the output 
b3 = Button(root, text = "DECRYPT", bg ="green", fg ="white", command = decryptMessage) 
b3.grid(row = 73, column = 15) 


root.mainloop() 