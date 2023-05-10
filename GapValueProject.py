from tkinter import *
from tkinter import ttk,messagebox
from ttkbootstrap import *
import numpy as np
import time
from math import ceil
import pickle


class window:
     st = {'Shell': False, 'Ciura': False, "Sedgewick": False,
          'Tokuda': False}  # to select the sorts
     def __init__(self, root, title) -> None:
          self.root = root
          self.root.title(title)
          self.root.resizable(width=False, height=False)
          Label(self.root, text='Shell Sort Gap Sequences').grid(
               row=0, columnspan=6)
          #  Buttons
          self.y = 0
          self.s = ttk.Button(self.root, text='Shell ', style='info.TButton', padding=5, width=15,
                              command=self.Shell)
          self.s.grid(column=0, row=1, padx=5, pady=5)
          self.cs = ttk.Button(self.root, text='Ciura', style='info.TButton', padding=5, width=15,
                              command=self.ciura)
          self.cs.grid(column=1, row=1, padx=5, pady=5)
          self.ss = ttk.Button(self.root, text='Sedgewick', style='info.TButton', padding=5, width=15,
                              command=self.sedgewick_seq)
          self.ss.grid(column=2, row=1, padx=5, pady=5)
          self.ts = ttk.Button(self.root, text='Tokuda', style='info.TButton', padding=5, width=15,
                              command=self.tokuda_seq)
          self.ts.grid(column=3, row=1, padx=5, pady=5)             
          self.start = ttk.Button(self.root, text='Start', padding=5, width=15,
                              command=self.start)
          self.start.grid(column=5, row=2, padx=5, pady=5)

          ttk.Label(self.root, text='Array Size:').grid(row=2,column=0)
          self.arraysize=ttk.Scale(self.root,from_=6,to=100,length=380,style='success.Horizontal.TScale',value=10,
               command=lambda x:self.slide_function())
          self.arraysize.grid(row=2,column=1,columnspan=3)
          
          ttk.Button(self.root, text='Reset', style='info.Outline.TButton', padding=5, width=15,
                                   command=self.reset).grid(column=5, row=1, padx=5, pady=5)
          ttk.Button(self.root, text='Test', style='info.Outline.TButton', padding=5, width=15,
                                   command=self.test).grid(column=4, row=2, padx=5, pady=5)
          ttk.Button(self.root, text='Mean', style='info.Outline.TButton', padding=5, width=15,
                                   command=self.mean).grid(column=4, row=1, padx=5, pady=5)

          #    Canvas
          self.canvas=Canvas(self.root, width=800, height=400,highlightbackground="dodgerblue",highlightthickness=2,
               bg='black')
          self.canvas.grid(row=4, padx=5, pady=10, columnspan=6)

          self.speed=.1
          self.N=10
          self.colours=['dodgerblue' for i in range(self.N)]
          N=self.N 
          self.data=np.linspace(5,400,N,dtype=np.uint16)
          np.random.shuffle(self.data)
          self.copy = self.data.copy()
          self.display(N,self.data,self.colours)
        
     
     def display(self,N: int,a: list,rong: list):
          '''
          N = number of rectangles
          a = array of heights of rectangles
          rong = array of colours of each and every rectangle'''

          self.canvas.delete('all')
          width=(1570)/(3*N-1)
          gap=width/2

          for i in range(N):
               self.rects = self.canvas.create_rectangle(7+i*width+i*gap,0,7+(i+1)*width+i*gap,a[i],fill=rong[i])

          self.root.update_idletasks()

     def slide_function(self):
          #Slide function
          self.N=int(self.arraysize.get())
          self.data=np.linspace(5,400,self.N,dtype=np.uint16)
          self.colours=['dodgerblue' for _ in range(self.N)]
          self.shuffle()
          
  
     def shuffle(self):
          #Shuffles/randomizes the array
          self.canvas.delete('all')
          self.data=np.linspace(5,400,self.N,dtype=np.uint16)
          np.random.shuffle(self.data)
          self.copy = self.data.copy()
          self.display(self.N,self.data,self.colours)

     def reset(self):
          #Button used after sorted: resets the sorted array to the original
          self.canvas.delete('all')
          self.data = self.copy.copy()
          self.display(self.N,self.copy,self.colours)
     
     def save(self,filename):
          #Primary function to save the array size and time given a filename
          my_dict = {}
          try:
               with open(filename, 'rb') as f:
                    # Load the data from the file only if the file is not empty
                    if f.seek(0, 2) != 0:
                         f.seek(0)
                         my_dict = pickle.load(f)
          except FileNotFoundError or PermissionError:
               messagebox.showerror("Error!", "Please change your directory to read the files")
          if self.N in my_dict:
               my_dict[self.N].append(self.y)
          else:
               my_dict[self.N] = [self.y]
          with open(filename, 'wb') as f:
               pickle.dump(my_dict, f)

     def read_for_mean(self,filename):
          #Returns mean and entries with a given filename, this is called by the mean function which displays the parts of this information
          try:
               with open(filename, 'rb') as f:
                    my_dict = pickle.load(f)
          except FileNotFoundError or UnboundLocalError:
               messagebox.showerror("Error!", "Please change your directory to read the files")
          if self.N in my_dict:
               values = my_dict[self.N]
               entries = len(values)
               int_values = [float(s) for s in values]
               mean = sum(int_values) / len(int_values)
               mean = "{:.1f}".format(mean)
               return mean, entries 
          else: return None, None
          
     def mean(self):
          """Returns the mean as a message"""
          shell, entries = self.read_for_mean('shell.txt')
          ciura, entries2 = self.read_for_mean('ciura.txt')
          sedgewick, entries3 = self.read_for_mean('sedgewick.txt')
          tokuda, entries4 = self.read_for_mean('tokuda.txt')
          messagebox.showinfo(title="Mean", message=f"Array Size: {self.N} \n Mean Times For \n Shell: {shell} Seconds, {entries} Entries \n Ciura {ciura} Seconds, {entries2} Entries \n Sedgewick: {sedgewick} Seconds, {entries3} Entries \n Tokuda: {tokuda} Seconds, {entries4} Entries")
          
     
               

     def test(self):
          #Continuously sorts same arrays with different sequences and then randomizes the array and repeats the process
          msg = messagebox.askokcancel("Testing", "Are You Sure You Want To Test?", icon = "question")
          if msg == True:
               for i in range(5):
                    self.shuffle()
                    self.shellsort(self.data,self.N)
                    self.display(self.N,self.data,['lime' for _ in range(self.N)])
                    self.save('shell.txt')
                    self.reset()
                    self.ciura_sort(self.data,self.N)
                    self.display(self.N,self.data,['lime' for _ in range(self.N)])
                    self.save('ciura.txt')
                    self.reset()
                    self.sedgewick(self.data,self.N)
                    self.display(self.N,self.data,['lime' for _ in range(self.N)])
                    self.save('sedgewick.txt')
                    self.reset()
                    self.tokuda(self.data,self.N)
                    self.save('tokuda.txt')
                    self.display(self.N,self.data,['lime' for _ in range(self.N)])
                    self.shuffle()
               self.mean()

     def msg(self): 
          #displays msges for each sequence time
          messagebox.showinfo(title="Sort Info", message=f"Time: {self.y} Seconds \n Array Size: {self.N} \n Gaps: {self.gaps}")


     # ---------------button selection of sequences---------------------------
     def Shell(self):
          if self.st['Shell'] is False:
               self.st['Shell'] = True
               self.s.config(style='success.TButton')

               for i in self.st:
                    if i != 'Shell':
                         self.st[i]=False

               self.ts.config(style='info.TButton')
               self.ss.config(style='info.TButton')
               self.cs.config(style='info.TButton')
              
          else:
               self.st['Shell'] = False
               self.s.config(style='info.TButton')
               

     def tokuda_seq(self):
          if self.st['Tokuda'] is False:
               self.st['Tokuda'] = True
               self.ts.config(style='success.TButton')

               for i in self.st:
                    if i != 'Tokuda':
                         self.st[i]=False

               self.s.config(style='info.TButton')
               self.ss.config(style='info.TButton')
               self.cs.config(style='info.TButton')
               
          else:
               self.st['Tokuda'] = False
               self.ts.config(style='info.TButton')
               

     def sedgewick_seq(self):
          if self.st["Sedgewick"] is False:
               self.st["Sedgewick"] = True
               self.ss.config(style='success.TButton')

               for i in self.st:
                    if i != "Sedgewick":
                         self.st[i]=False

               self.s.config(style='info.TButton')
               self.ts.config(style='info.TButton')
               self.cs.config(style='info.TButton')
               
          else:
               self.st["Sedgewick"] = False
               self.ss.config(style='info.TButton')
               

     def ciura(self):
          if self.st['Ciura'] is False:
               self.st['Ciura'] = True
               self.cs.config(style='success.TButton')


               for i in self.st:
                    if i != 'Ciura':
                         self.st[i]=False
               self.s.config(style='info.TButton')
               self.ss.config(style='info.TButton')
               self.ts.config(style='info.TButton')
               
          else:
               self.st['Ciura'] = False
               self.cs.config(style='info.TButton')
 
     # --------------------Play---------------------------------------
     

     def start(self):
          if self.st['Shell'] is True:
               self.shellsort(self.data,self.N)
               self.display(self.N,self.data,['lime' for _ in range(self.N)])
               self.msg()

          elif self.st['Ciura'] is True:
               self.ciura_sort(self.data,self.N)
               self.display(self.N,self.data,['lime' for _ in range(self.N)])
               self.msg()

          elif self.st["Sedgewick"] is True:
               self.sedgewick(self.data,self.N)
               self.display(self.N,self.data,['lime' for _ in range(self.N)])
               self.msg()

          elif self.st['Tokuda'] is True:
               self.tokuda(self.data,self.N-1)
               self.display(self.N,self.data,['lime' for _ in range(self.N)])
               self.msg()

          else:
               #show messege box
               messagebox.showerror("Woops!", "You didn't select any sequences")
               

     # -----------Shell Sort-------------------------------------
     def shellsort(self,a,size):
          self.gaps = []
          start_time = time.time()
          gap = size//2
          self.gaps.append(gap)
          while gap > 0:
               for i in range(gap, size):

                    temp = a[i]
                    j = i
                    while j >= gap and a[j - gap] > temp:
                         a[j] = a[j - gap]
                         j -= gap
                         self.display(self.N,self.data,['yellow' if x==j or x == i else 'dodgerblue' for x in range(self.N)])
                         time.sleep(self.speed)
                    a[j] = temp
               gap //= 2
               self.gaps.append(gap)

          end_time = time.time()
          x = end_time - start_time
          self.y = "{:.1f}".format(x)
          
     # -----------Ciura Sort-------------------------------------
     def ciura_sort(self,a,size):
          start_time = time.time()
          self.gaps = [701, 301, 132, 57, 23, 10, 4, 1]
          for value in self.gaps:
               for i in range(value, size):
                    temp = a[i]
                    j = i
                    while j >= value and a[j - value] > temp:
                         a[j] = a[j - value]
                         j -= value
                         self.display(self.N,self.data,['pink' if x==j or x == i else 'dodgerblue' for x in range(self.N)])
                         time.sleep(self.speed)
                    a[j] = temp
          end_time = time.time()
          x = end_time - start_time
          self.y = "{:.1f}".format(x)
# -----------Sedgewick Sort-------------------------------------
     def sedgewick(self,a,size):
          start_time = time.time()
          self.gaps = []
          i = 0
          while True:
               if i % 2 == 0:
                    gap = 9 * (2**i - 2**(i//2)) + 1
               else:
                    gap = 8 * 2**i - 6 * 2**((i+1)//2) + 1
               i += 1
               if gap >= size:
                    break
               self.gaps.append(gap)

          for gap in reversed(self.gaps):
               for i in range(gap, size):
                    temp = a[i]
                    j = i
                    while j >= gap and a[j-gap] > temp:
                         a[j] = a[j-gap]
                         j -= gap
                         self.display(self.N,self.data,['purple' if x==j or x == i else 'dodgerblue' for x in range(self.N)])
                         time.sleep(self.speed)
                    a[j] = temp
          end_time = time.time()
          x = end_time - start_time
          self.y = "{:.1f}".format(x)


     #----------------Tokuda Sort----------------------------------
     def tokuda(self, a, size):
          self.gaps = []
          start_time = time.time()
          k = 1
          while True:
               gap = math.ceil((1/5)*(9*(9/4)**(k-1)-4))
               self.gaps.append(gap)
               k += 1
               if gap >= size:
                    break

          for gap in reversed(self.gaps):
               for i in range(gap, len(a)):
                    temp = a[i]
                    j = i
                    while j >= gap and a[j - gap] > temp:
                         a[j] = a[j - gap]
                         j -= gap
                         self.display(self.N, self.data, ['red' if x == j or x == i else 'dodgerblue' for x in range(self.N)])
                         time.sleep(self.speed)
                    a[j] = temp

          end_time = time.time()
          x = end_time - start_time
          self.y = "{:.1f}".format(x)
          


          


if __name__ == '__main__':
     win = Style(theme='darkly').master
     obj = window(win, 'Shell Sort by Aaron, Jesus, and Cole')
     win.mainloop()
