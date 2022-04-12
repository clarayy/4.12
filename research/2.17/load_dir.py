import os

bmname = 'dolphins_p0.5_m10_test'

dir = '/home/iot/zcy/usb/copy/MINIST/MINIST/mydata/'+bmname+'/'+bmname+'_adjdata/'

files = os.listdir(dir)
files.sort(key=lambda x:int(x[:-4])) 
filename_train = '/home/iot/zcy/usb/copy/MINIST/MINIST/mydata/'+bmname+'/train.txt'
filename_test = '/home/iot/zcy/usb/copy/MINIST/MINIST/mydata/'+bmname+'/test.txt'
train = open(filename_test,'a')
for file in files:
    fileType = os.path.split(file)
    if fileType[1] == '.txt':
        continue
    name =  str(dir) +  file + ' ' + str(int(fileType[1][:-4])//100) +'\n'
    train.write(name)
# val = open(filename_val, 'a')
# i = 1
# for file in files:
#     if i<1600:
#         fileType = os.path.split(file)
#         if fileType[1] == '.txt':
#             continue
#         name =  str(dir) +  file + ' ' + str(int(fileType[1][:-4])//100) +'\n'
#         train.write(name)
#         i = i+1
#         print(i)
#     else:
#         fileType = os.path.split(file)
#         if fileType[1] == '.txt':
#             continue
#         name = str(dir) +file + ' ' + str(int(fileType[1][:-4])//100) +'\n'
#         val.write(name)
#         i = i+1
#         print(i)
# val.close()
train.close()

