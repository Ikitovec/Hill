from tkinter import *
from tkinter import scrolledtext
from tkinter.ttk import Combobox
from tkinter import messagebox
import numpy as np
import math


def clicked():
    txt_original = txt.get("1.0", 'end-1c').lower()
    txt2.delete(1.0, END)
    eng_alphabet='abcdefghijklmnopqrstuvwxyz .?'
    rus_alphabet='абвгдеёжзийклмнопрстуфхцчшщъыьэюя .,?'
    key=txt3.get("1.0", 'end-1c').lower()

    index=0
    alphabet=eng_alphabet
    for i in txt_original:
        if (i!=' ') & (i!='.') & (i!='?'):
            for j in range(0, 1):
                    index = eng_alphabet.find(i, 0)
                    if (index != -1):
                        alphabet = eng_alphabet
                        break
                    if (index == -1):
                            index = rus_alphabet.find(i, 0)
                            if (index != -1):
                                alphabet = rus_alphabet
                                break

    for i in key:
        if alphabet.find(i)==-1:
            print(f'проверьте правильность ключа в ключе могут содержаться лишь символы {alphabet}')
            break


    #проверяем правильность ввода маски

    n_gramm=math.ceil(math.sqrt(len(key)))
    if len(key)==0:
        print('Маска должна быть ненулевой!')

    else:
        mask=[0]*n_gramm
        for i in range (len(mask)):
            mask[i]=[0]*n_gramm


        count=0
        for i in range (len(mask)):
            for j in range (len(mask[i])):

                    mask[i][j]=alphabet.find(str(key[(i*len(mask)+j)%len(key)]))
                    count+=1
        print('mask=',mask)

        mask=np.array(mask)
        if np.linalg.det(mask)==0:
            print('Выберите другой ключ!')
        else:

            if combo2.get() == 'Зашифровать':
                count=0
                A=[0]*n_gramm
                alp_count=0
                for i in txt_original:
                    A[count%n_gramm]=alphabet.find(i)
                    count+=1
                    alp_count+=1
                    if ((count % n_gramm ==0)| (alp_count==len(txt_original))):

                        secret=np.array(A)
                        secret_key=np.array(mask)

                        c=secret.dot(secret_key) % len(alphabet)
                        print(c)
                        for index in range(len(c)):
                            txt2.insert(INSERT, alphabet[c[index]])


                        count=0
                        A=[0]*n_gramm


            #расшифровка
            if combo2.get() == 'Расшифровать':
                alp_count = 0
                mask_inv = np.linalg.inv(mask)
                print('-----------------')
                print(mask)
                print('mask_inv=',mask_inv)
                det = round(np.linalg.det(mask))
                print('DETERMINANT',det)
                print(mask_inv * det % len(alphabet))

                temp_i = 1
                flag = 0
                while flag != 1:
                    if (temp_i * det) % len(alphabet) == 1:
                        flag = 1
                    else:
                        temp_i += 1

                #print(((mask_inv * det) * temp_i) % len(alphabet))
                new_mask=((mask_inv * det) * temp_i) % len(alphabet)
                print(new_mask)
                count = 0
                A = [0] * n_gramm
                for i in txt_original:
                    A[count % n_gramm] = alphabet.find(i)
                    count += 1
                    alp_count +=1
                    if ((count % n_gramm == 0) | (alp_count==len(txt_original))):

                        secret = np.array(A)
                        secret_key = new_mask
                        c = secret.dot(secret_key) % len(alphabet)
                        print('-------',c)
                        #print(c[0],c[1],c[2])
                        #print(alphabet)

                        for index in range(len(c)):
                            txt2.insert(INSERT, alphabet[round(c[index]) % len(alphabet)])
                            #print(math.ceil(int(c[index])))

                        count = 0
                        A = [0] * n_gramm

def swap():
    temp = txt2.get("1.0", 'end-1c')
    txt.delete(1.0, END)
    txt.insert(INSERT, temp)
    txt2.delete(1.0, END)

window = Tk()
window.title("Шифр Хилла")
window.geometry('500x250')

lbl = Label(window, text="Ключ")
lbl.grid(column=0, row=2)

txt3 = scrolledtext.ScrolledText(window, width=40, height=1)
txt3.grid(column=2, row=2)


combo2 = Combobox(window)
combo2['values'] = ("Зашифровать", "Расшифровать")
combo2.current(0)
combo2.grid(column=0, row=4)



btn = Button(window, text="Получить ответ", command=clicked)
btn.grid(column=0, row=5)
lbl = Label(window)


btn = Button(window, text="Поменять значения", command=swap)
btn.grid(column=2, row=4)
lbl = Label(window)

lbl = Label(window, text="Ваше сообщение")
lbl.grid(column=0, row=0)

txt = scrolledtext.ScrolledText(window, width=40, height=1)
txt.grid(column=2, row=0)


lbl = Label(window, text="Результат:")
lbl.grid(column=0, row=6)


txt2 = scrolledtext.ScrolledText(window, width=40, height=1)
txt2.grid(column=2, row=6)


window.mainloop()

