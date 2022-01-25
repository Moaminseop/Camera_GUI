from scipy.ndimage import gaussian_filter1d
import cv2, sys, os, math, numpy
from PyQt5.QtCore import QThread
from ui_function import LoadingScreen

class ResFuncThread(QThread):
    def __init__(self, parent):
        super().__init__(parent)

    def testRes(self, imgAddress, start, end, line , direction): # 이미지 주소와 ROI의 좌상단픽셀, ROI의 우하단픽셀위치, 줄 수,검사방향을 입력받습니다.
        img = cv2.imread(imgAddress)
        height, width, channel = img.shape
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        result = [] # 1 or 0 으로 각 영역의 pass or fail 여부를 의미합니다.
        for x in range(len(start)):
            result.append(1)

        countedlimit = []  # 해상력 한계치의 좌표를 의미합니다.
        for x in range(len(start)):
            countedlimit.append([])

        # 흑백으로 변환된 이미지로부터 픽셀 밝기의 범위중앙값을 계산합니다. (white255, black0)
        min = 255
        max = 0
        for y in range(0, height):
            for x in range(0, width):
                if (img_gray[y,x] > max):
                    max = img_gray[y,x]
                if (img_gray[y,x] < min):
                    min = img_gray[y,x]
        mean = int((min+max)/2)

        # ROI의 좌측상단에서 세로로 한줄씩 오른쪽으로 이동하며 해상력을 테스트합니다.

        for i in range(len(start)):
            if (direction[i] == 1): # 검사방향 : 왼쪽 > 오른쪽
                countedline = 0
                # 한 줄만이라도 모든 판단선을 검출하지 못했을시 break
                for x in range(start[i][0], end[i][0]):
                    countedline = 0
                    countedlimit[i] = x
                    for y in range(start[i][1], end[i][1]):
                        if ((img_gray[y-1,x]>mean) and (img_gray[y,x]<=mean)):
                            countedline+=1
                    if countedline<line[i]:
                        if(x < (start[i][0]+end[i][0])/2):
                            result[i]=0
                        # else:
                        #     result[i]=[1]
                        break

            if (direction[i] == 2): # 검사방향 : 오른쪽 > 왼쪽
                countedline = 0
                # 한 줄만이라도 모든 판단선을 검출하지 못했을시 break
                for x in range(end[i][0], start[i][0], -1):
                    countedline = 0
                    countedlimit[i] = x
                    for y in range(start[i][1], end[i][1]):
                        if ((img_gray[y-1,x]>mean) and (img_gray[y,x]<=mean)):
                            countedline+=1
                    if countedline<line[i]:
                        if(x > (start[i][0]+end[i][0])/2):
                            result[i]=0
                        # else:
                        #     result[i]=[1]
                        break

            if (direction[i] == 3): # 검사방향 : 위 > 아래
                countedline = 0
                # 한 줄만이라도 모든 판단선을 검출하지 못했을시 break
                for y in range(start[i][1], end[i][1]):
                    countedline = 0
                    countedlimit[i] = y
                    for x in range(start[i][0], end[i][0]):
                        if ((img_gray[y,x-1]>mean) and (img_gray[y,x]<=mean)):
                            countedline+=1
                    if countedline<line[i]:
                        if(y < (start[i][1]+end[i][1])/2):
                            result[i]=0
                        # else:
                        #     result[i]=[1]
                        break

            if (direction[i] == 4): # 검사방향 : 아래 > 위
                countedline = 0
                # 한 줄만이라도 모든 판단선을 검출하지 못했을시 break
                for y in range( end[i][1],start[i][1],-1):
                    countedline = 0
                    countedlimit[i] = y
                    for x in range(start[i][0], end[i][0]):
                        if ((img_gray[y,x-1]>mean) and (img_gray[y,x]<=mean)):
                            countedline+=1
                    if countedline<line[i]:
                        if(y > (start[i][1]+end[i][1])/2):
                            result[i]=0
                        # else:
                        #     result[i]=[1]
                        break

        # 계산된 countedx와 ROI를 그림에 표시합니다.
        for i in range(len(start)):
            cv2.rectangle(img, start[i], end[i], (0, 255, 0), thickness = 3)
            if (direction[i] == 1) or (direction[i] == 2):
                for y in range(start[i][1], end[i][1]):
                    img[y, countedlimit[i]] = 255,0,0
                    img[y, int((start[i][0]+end[i][0])/2)] = 0,255,0
            elif (direction[i] == 3) or (direction[i] == 4):
                for x in range(start[i][0], end[i][0]):
                    img[countedlimit[i],x] = 255,0,0
                    img[int((start[i][1] + end[i][1])/2), x] = 0,255,0

        # cv.imshow(imgAddress, img)
        # cv2.imwrite("./data/resresult.png", img)

        pf = 0
        for i in range(len(result)):
            pf = result[i]
            
        return img, pf



class VignetFuncThread(QThread):
    def __init__(self):
        super().__init__()

    def check_monotonically_increase(self, parameter_tup):
        """a, b, c가 [0,1]에서 g(r)를 단조롭게 증가시킬 수 있는지 확인한다."""

        a, b, c = parameter_tup
        if c == 0:
            if a >= 0 and a + 2 * b >= 0 and not(a == 0 and b == 0):
                return True
            return False
        if c < 0:
            if b**2 > 3 * a * c:
                q_plus = (-2 * b + math.sqrt(4 * b**2 - 12 * a * c)) / (6 * c)
                q_minus = (-2 * b - math.sqrt(4 * b**2 - 12 * a * c)) / (6 * c)
                if q_plus <= 0 and q_minus >= 1:
                    return True
            return False
        if c > 0:
            if b**2 < 3 * a * c:
                return True
            elif b**2 == 3 * a * c:
                if b >= 0 or 3 * c + b <= 0:
                    return True
            else:
                q_plus = (-2 * b + math.sqrt(4 * b**2 - 12 * a * c)) / (6 * c)
                q_minus = (-2 * b - math.sqrt(4 * b**2 - 12 * a * c)) / (6 * c)
                if q_plus <= 0 or q_minus >= 1:
                    return True
            return False


    def calc_discrete_entropy(self, cm_x, cm_y, max_distance, parameter_tup, im):
        """
        주어진 파라미터의 게인 함수로 사진의 밝기를 조절한 후 이산 엔트로피를 계산한다.
        """

        print(parameter_tup)

        a, b, c = parameter_tup
        row, col = im.shape

        histogram = [0 for i in range(256)]

        for i in range(col):
            for j in range(row):

                # 현재 픽셀에서 사진의 질량 중심까지의 거리와 해당하는 r 값을 계산합니다.
                distance = math.sqrt((i - cm_x)**2 + (j - cm_y)**2)
                r = distance / max_distance

                # 게인 함수 평가 및 픽셀 밝기 값 조정
                g = 1 + a * r**2 + b * r**4 + c * r**6
                intensity = im[j, i] * g

                # 밝기 값을 해당 히스토그램 빈에 매핑합니다
                bin = 255 * math.log(1 + intensity) / math.log(256)
                floor_bin = math.floor(bin)
                ceil_bin = math.ceil(bin)

                # 조정 후 밝기 값이 255를 초과하는 경우, 상단 끝에 히스토그램 빈을 추가하기만 하면 됩니다.
                if bin > len(histogram) - 1:
                    for k in range(len(histogram), ceil_bin + 1):
                        histogram.append(0)

                histogram[floor_bin] += 1 + floor_bin - bin
                histogram[ceil_bin] += ceil_bin - bin

        # Gausssian 커널을 사용하여 히스토그램 평활
        histogram = gaussian_filter1d(histogram, 4)

        histogram_sum = sum(histogram)
        H = 0

        # Calculate discrete entropy
        for i in range(len(histogram)):
            p = histogram[i] / histogram_sum
            if p != 0:
                H += p * math.log(p)

        return -H


    def find_parameters(self, cm_x, cm_y, max_distance, im):
        """
        이미지의 질량 중심과 이미지의 가장 먼 꼭짓점에서 질량 중심까지의 거리를 고려할 때 이미지의 엔트로피를 최소화할 수 있는 a, b, c를 찾습니다.
        """

        a = b = c = 0
        delta = 2
        min_H = None

        # 실행시간 최소화하기 위해 탐색 세트 설정
        explored = set()

        while delta > 1 / 256:
            initial_tup = (a, b, c)

            for parameter_tup in [(a + delta, b, c), (a - delta, b, c),
                                (a, b + delta, c), (a, b - delta, c),
                                (a, b, c + delta), (a, b, c - delta)]:

                if parameter_tup not in explored:
                    explored.add(parameter_tup)

                    if self.check_monotonically_increase(parameter_tup):
                        curr_H = self.calc_discrete_entropy(
                            cm_x, cm_y, max_distance, parameter_tup, im)

                        # if the entropy is lower than current minimum, set parameters to current ones
                        if min_H is None or curr_H < min_H:
                            min_H = curr_H
                            a, b, c = parameter_tup

            # if the current parameters minimize the entropy with the current delta, reduce the delta
            if initial_tup == (a, b, c):
                delta /= 2

        return a, b, c


    def vignetting_correction(self, imgAddress):
        """
        이산 엔트로피를 최소화할 수 있는 파라미터를 사용하여 영상의 vigneting을 수정합니다.
        """
        #self.ld = LoadingScreen()
        im = cv2.imread(imgAddress)

        # RGB이미지를 grayscale로 변경
        imgray = cv2.transform(im, numpy.array([[0.2126, 0.7152, 0.0722]]))
        row, col = imgray.shape

        # 그림의 무게 중심 계산
        cm_x = sum(j * imgray[i, j] for i in range(row) for j in range(col)
                ) / sum(imgray[i, j] for i in range(row) for j in range(col))
        cm_y = sum(i * imgray[i, j] for i in range(row) for j in range(col)
                ) / sum(imgray[i, j] for i in range(row) for j in range(col))
        max_distance = math.sqrt(max(
            (vertex[0] - cm_x)**2 + (vertex[1] - cm_y)**2 for vertex in [[0, 0], [0, row], [col, 0], [col, row]]))

        # 이미지 크기가 너무 큰 경우 축소 이미지를 사용하여 파라미터를 가져오고 초기 이미지에 적용하여 실행 시간을 절약합니다.
        if col > 500:
            ratio = col / 500
            imgray_sm = cv2.resize(imgray, (500, round(row / ratio)))
            a, b, c = self.find_parameters(
                cm_x / ratio, cm_y / ratio, max_distance / ratio, imgray_sm)
        else:
            a, b, c = self.find_parameters(cm_x, cm_y, max_distance, imgray)

        # 원래 이미지 수정 및 비네팅 여부 판별
        judgment = 0
        for i in range(col):
            for j in range(row):
                distance = math.sqrt((i - cm_x)**2 + (j - cm_y)**2)
                r = distance / max_distance
                g = 1 + a * r**2 + b * r**4 + c * r**6
                if(g > 2): judgment += 1
                for k in range(3):
                    modified = im[j, i][k] * g

                    # 수정 후 밝기가 255보다 크면 255로 설정합니다.
                    if modified > 255:
                        modified = 255
                    im[j, i][k] = modified
        
        #self.ld.endAnimation()
        if(judgment >= 1):
            print("비네팅이 존재하여 수정 하여 저장하였습니다.")
            pf = 0
            #cv2.imwrite("./data/vignette_result.png", im) #저장하기
        else :
            print("비네팅이 없습니다.")
            pf = 1
        
        return im, pf

class EdgeFuncThread(QThread):
    def __init__(self, parent):
        super().__init__(parent)


    def testRes(self, imgAddress): # 이미지 주소와 ROI의 좌상단픽셀, ROI의 우하단픽셀위치를 입력받습니다.
        img = cv2.imread(imgAddress)
        height, width, channel = img.shape
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        #ROI의 좌표set을 const로 정의해놓음. 순서는 [좌상, 우상, 좌하, 우하, 중앙] 입니다
        ROI_X = [(13,40), (1018,40), (13,515), (1018,515), (514, 276)]
        ROI_Y = [(68,95), (1073,95), (68,570), (1073,570), (572, 334)]

        #Pass/Fail의 기준이 되는 value의 list
        SET_VALUE = [45,45,45,45,390]

        # 흑백으로 변환된 이미지로부터 픽셀 밝기의 범위중앙값을 계산합니다. (white255, black0)
        min = 255
        max = 0
        for y in range(0, height):
            for x in range(0, width):
                if (img_gray[y,x] > max):
                    max = img_gray[y,x]
                if (img_gray[y,x] < min):
                    min = img_gray[y,x]
        mean = int((min+max)/2)

        # ROI의 좌측상단에서 가로로 한줄씩 오른쪽으로 이동하며 픽셀값을 비교합니다.
        countedline = [0,0,0,0,0]

        for i in range (0,5):
            for y in range(ROI_X[i][1], ROI_Y[i][1]):
                state = 0 #state를 0으로 초기화합니다.
                for x in range(ROI_X[i][0], ROI_Y[i][0]):
                    if ((img_gray[y,x-1]>mean) and (img_gray[y,x]<=mean)):
                        state = 1 #픽셀값이 mean값아래로 떨어질때 state를 1로 설정합니다.
                    elif (((img_gray[y,x-1]<=mean) and (img_gray[y,x]>mean)) and (state == 1)):
                        countedline[i] += 1 #state값이 1이고 픽셀값이 mean값 이상으로 올라갈때 countedline을 1 증가시킵니다.

        
        #기준치와 비교해서 passFail 변수에 pass/fail 여부 저장하시
        for i in range (0,5):
            if(countedline[i] > SET_VALUE[i]): 
                passFail = "Pass"
                pf = 1

            else:
                passFail = "Fail"
                pf = 0

        # 계산된 countedx와 ROI를 그림에 표시합니다.
            cv2.rectangle(img, ROI_X[i], ROI_Y[i], (0, 0, 255), thickness = 2)
            cv2.putText(img, str(countedline[i]), ROI_X[i], cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            cv2.putText(img, passFail, (ROI_X[i][0],ROI_Y[i][1]+21), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        

        return img, pf
