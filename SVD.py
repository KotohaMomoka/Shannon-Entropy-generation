import numpy as np
import os
import linecache
import csv
from itertools import permutations


def get_line(file, nums_line):
    return linecache.getline(file, nums_line).strip()

def po2co(x):
    return int(x * 4 - 1)
class get_position(object):
    XX = []
    YY = []
    ZZ = []
    EElement = []
    num = []
    matrix_x1 = np.zeros([4, 4], dtype=int)
    matrix_x2 = np.zeros([4, 4], dtype=int)
    matrix_y1 = np.zeros([4, 4], dtype=int)
    matrix_y2 = np.zeros([4, 4], dtype=int)
    matrix_z1 = np.zeros([4, 4], dtype=int)
    matrix_z2 = np.zeros([4, 4], dtype=int)
    Entropy_shonon = []

    def get_file(self, file):
        ELEMENT = get_line(file, 6).split()
        NUM = get_line(file, 7).split()
        numbers = [1, 2, 3, 4, 5, 6]
        permutations_list = list(permutations(numbers))
        permutations_num = len(permutations_list)
        for k in range(permutations_num):
            for i in range(len(ELEMENT)):
                for j in range(int(NUM[i])):
                    if ELEMENT[i] == 'Fe':
                        self.EElement.append('Fe')
                        self.num.append(permutations_list[k][0])
                    if ELEMENT[i] == 'Co':
                        self.EElement.append('Co')
                        self.num.append(permutations_list[k][1])
                    if ELEMENT[i] == 'Ni':
                        self.EElement.append('Ni')
                        self.num.append(permutations_list[k][2])
                    if ELEMENT[i] == 'Al':
                        self.EElement.append('Al')
                        self.num.append(permutations_list[k][3])
                    if ELEMENT[i] == 'Ti':
                        self.EElement.append('Ti')
                        self.num.append(permutations_list[k][4])
                    if ELEMENT[i] == 'Cu':
                        self.EElement.append('Cu')
                        self.num.append(permutations_list[k][5])
            for line in range(9, 41):
                positionx = get_line(file, line).split()
                x = float(positionx[0])
                y = float(positionx[1])
                z = float(positionx[2])
                self.XX.append(x)
                self.YY.append(y)
                self.ZZ.append(z)
            self.gen_matrix_x()
            self.gen_matrix_y()
            self.gen_matrix_z()
            self.relex()
            self.svd()
    def gen_matrix_x(self):
        x1 = []
        x2 = []
        y1 = []
        y2 = []
        z1 = []
        z2 = []
        num1 = []
        num2 = []
        for i in range(0, 32):
            if self.XX[i] <= 0.5:
                x1.append(self.XX[i])
                y1.append(self.YY[i])
                z1.append(self.ZZ[i])
                num1.append(self.num[i])
            else:
                x2.append(self.XX[i])
                y2.append(self.YY[i])
                z2.append(self.ZZ[i])
                num2.append(self.num[i])
        for j in range(0, 16):
            yy1 = po2co(y1[j])
            zz1 = po2co(z1[j])
            yy2 = po2co(y2[j])
            zz2 = po2co(z2[j])
            self.matrix_x1[yy1][zz1] = num1[j]
            self.matrix_x2[yy2][zz2] = num2[j]
    def gen_matrix_y(self):
        x1 = []
        x2 = []
        y1 = []
        y2 = []
        z1 = []
        z2 = []
        num1 = []
        num2 = []
        for i in range(0, 32):
            if self.YY[i] <= 0.5:
                x1.append(self.XX[i])
                y1.append(self.YY[i])
                z1.append(self.ZZ[i])
                num1.append(self.num[i])
            else:
                x2.append(self.XX[i])
                y2.append(self.YY[i])
                z2.append(self.ZZ[i])
                num2.append(self.num[i])
        for j in range(0, 16):
            xx1 = po2co(x1[j])
            zz1 = po2co(z1[j])
            xx2 = po2co(x2[j])
            zz2 = po2co(z2[j])
            self.matrix_y1[xx1][zz1] = num1[j]
            self.matrix_y2[xx2][zz2] = num2[j]

    def gen_matrix_z(self):
        x1 = []
        x2 = []
        y1 = []
        y2 = []
        z1 = []
        z2 = []
        num1 = []
        num2 = []
        for i in range(0, 32):
            if self.ZZ[i] <= 0.5:
                x1.append(self.XX[i])
                y1.append(self.YY[i])
                z1.append(self.ZZ[i])
                num1.append(self.num[i])
            else:
                x2.append(self.XX[i])
                y2.append(self.YY[i])
                z2.append(self.ZZ[i])
                num2.append(self.num[i])
        for j in range(0, 16):
            xx1 = po2co(x1[j])
            yy1 = po2co(y1[j])
            xx2 = po2co(x2[j])
            yy2 = po2co(y2[j])
            self.matrix_z1[xx1][yy1] = num1[j]
            self.matrix_z2[xx2][yy2] = num2[j]

    def svd(self):
        sigma_xx1 = []
        sigma_xx2 = []
        sigma_yy1 = []
        sigma_yy2 = []
        sigma_zz1 = []
        sigma_zz2 = []
        U1, sigma_x1, VT1 = np.linalg.svd(self.matrix_x1)
        U2, sigma_x2, VT2 = np.linalg.svd(self.matrix_x2)
        U3, sigma_y1, VT3 = np.linalg.svd(self.matrix_y1)
        U4, sigma_y2, VT4 = np.linalg.svd(self.matrix_y2)
        U5, sigma_z1, VT5 = np.linalg.svd(self.matrix_z1)
        U6, sigma_z2, VT6 = np.linalg.svd(self.matrix_z2)

        for i in range(0, 4):
            xx1 = sigma_x1[i] / sum(sigma_x1)
            xx2 = sigma_x2[i] / sum(sigma_x2)
            yy1 = sigma_y1[i] / sum(sigma_y1)
            yy2 = sigma_y2[i] / sum(sigma_y2)
            zz1 = sigma_z1[i] / sum(sigma_z1)
            zz2 = sigma_z2[i] / sum(sigma_z2)
            if xx1 == 0:
                sigma_xx1.append(1)
            else:
                sigma_xx1.append(xx1)
            if xx2 == 0:
                sigma_xx2.append(1)
            else:
                sigma_xx2.append(xx2)
            if yy1 == 0:
                sigma_yy1.append(1)
            else:
                sigma_yy1.append(yy1)
            if yy2 == 0:
                sigma_yy2.append(1)
            else:
                sigma_yy2.append(yy2)
            if zz1 == 0:
                sigma_zz1.append(1)
            else:
                sigma_zz1.append(zz1)
            if zz2 == 0:
                sigma_zz2.append(1)
            else:
                sigma_zz2.append(zz2)
        shonon_x1 = - sigma_xx1[0] * np.log2(sigma_xx1[0]) \
                    - sigma_xx1[1] * np.log2(sigma_xx1[1]) \
                    - sigma_xx1[2] * np.log2(sigma_xx1[2]) \
                    - sigma_xx1[3] * np.log2(sigma_xx1[3])
        shonon_x2 = - sigma_xx2[0] * np.log2(sigma_xx2[0]) \
                    - sigma_xx2[1] * np.log2(sigma_xx2[1]) \
                    - sigma_xx2[2] * np.log2(sigma_xx2[2]) \
                    - sigma_xx2[3] * np.log2(sigma_xx2[3])
        shonon_y1 = -sigma_yy1[0] * np.log2(sigma_yy1[0]) \
                    - sigma_yy1[1] * np.log2(sigma_yy1[1]) \
                    - sigma_yy1[2] * np.log2(sigma_yy1[2]) \
                    - sigma_yy1[3] * np.log2(sigma_yy1[3])
        shonon_y2 = - sigma_yy2[0] * np.log2(sigma_yy2[0]) \
                    - sigma_yy2[1] * np.log2(sigma_yy2[1]) \
                    - sigma_yy2[2] * np.log2(sigma_yy2[2]) \
                    - sigma_yy2[3] * np.log2(sigma_yy2[3])
        shonon_z1 = - sigma_zz1[0] * np.log2(sigma_zz1[0]) \
                    - sigma_zz1[1] * np.log2(sigma_zz1[1]) \
                    - sigma_zz1[2] * np.log2(sigma_zz1[2]) \
                    - sigma_zz1[3] * np.log2(sigma_zz1[3])
        shonon_z2 = - sigma_zz2[0] * np.log2(sigma_zz2[0]) \
                    - sigma_zz2[1] * np.log2(sigma_zz2[1]) \
                    - sigma_zz2[2] * np.log2(sigma_zz2[2]) \
                    - sigma_zz2[3] * np.log2(sigma_zz2[3])
        self.Entropy_shonon.append(str(shonon_x1))
        self.Entropy_shonon.append(str(shonon_x2))
        self.Entropy_shonon.append(str(shonon_y1))
        self.Entropy_shonon.append(str(shonon_y2))
        self.Entropy_shonon.append(str(shonon_z1))
        self.Entropy_shonon.append(str(shonon_z2))

    def relex(self):
        self.XX.clear()
        self.YY.clear()
        self.ZZ.clear()
        self.EElement.clear()
        self.num.clear()

    def relex_shonnon(self):
        self.Entropy_shonon.clear()


path_3 = 'F:\study documents\code\ML_deal\Entropy_Shonon_exchange.csv'
csvfile = open(path_3, 'w+', newline='')
name = []
for k in range(720):
    name.append('Shannon_x1_' + str(k))
    name.append('Shannon_x2_' + str(k))
    name.append('Shannon_y1_' + str(k))
    name.append('Shannon_y2_' + str(k))
    name.append('Shannon_z1_' + str(k))
    name.append('Shannon_z2_' + str(k))
writer = csv.writer(csvfile)
writer.writerow(name)
# path1 = 'F:\study documents\code\ML_deal\计算数据'
# for i in range(1, 37):
#     path2 = 'Con' + str(i).zfill(2) + '\step1'
#     path_1 = os.path.join(path1, path2)
#     for j in range(0,20):
#         k = (i - 1) * 20 + j
#         path3 = '1_Index_' + str(k) + '\POSCAR'
#         path_2 = os.path.join(path_1, path3)
#         position = get_position()
#         position.get_file(path_2)
#         writer.writerow(position.Entropy_shonon)
#         position.relex_shonnon()
#         print('INDEX_', k)
# csvfile.close()
for i in range(1, 17):
    path1 = 'F:\study documents\code\ML_deal\exchange'
    path2 = str(i) + '.POSCAR'
    path_1 = os.path.join(path1, path2)
    position = get_position()
    position.get_file(path_1)
    writer.writerow(position.Entropy_shonon)
    position.relex_shonnon()
    print('INDEX_', i)
csvfile.close()