A = range(1, 11)
B = list(map(chr, range(ord('a'), ord('h')+1)))

def setout(A):
    if len(A) == 0:
        print("~")
        return
    print("{", end = "")
    for i in range(0, len(A)):
        if(i < len(A) - 1):
            print(A[i], ", ", end = "", sep = "")
    print(A[i], "}\n")

print("A = ", end = "")
setout(A)

print("B = ", end = "")
setout(B)

print("\nA ~")
for i in A:
    for j in B:
        print("(%d, %c), " %(i,j), end = " ")
print("\b\b }\n")


#=========================================

#행렬 입력

def main():
    A = [1, 2, 3, 4, 5]
    n = len(A)
    matrix = []
    print("5x5 관계행렬 입력 : ")
    for _ in range(n):
        row = list(map(int, input().split()))
        matrix.append(row)

#==============================================

#경로탐색

maxvalue = int(input("입력받을 관계행렬 크기 : "))
print("\n")
print("1과 0으로 구성된 ", maxvalue, "x", maxvalue, "인 관계행렬을 입력 : ", sep='')


data = []
while len(data) < maxvalue * maxvalue:
    data += input().split()

for i in range(1, maxvalue + 1):
    for j in range(1, maxvalue + 1):
        m[i][j] = int(data[(i - 1) * maxvalue + (j - 1)])

print("\n주어진 관계행렬에 대해 길이가 3인 경로들의 리스트는 다음과 같다.\n")
count = 0
for i in range(1, maxavalue + 1):
    for j in range(1, maxavalue + 1):
        if m[i][j] == 1:
            for x in range(1, maxavalue + 1):
                if m[j][x] == 1:
                    for y in range(1, maxavalue + 1):
                        if m[x][y] == 1:
                            print("~")
                            count += 1

if count == 0:
    print("주어진 행렬에 대해 길이가 3인 경로 없음")

#========================================================

#반사관계

    #표에서 1인 순서쌍 추출 및 출력
def print_reflection(matrix, A):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 1:
                print(f"({A[i]}, {A[j]}", end=" ")

    #주대각 원소가 1임을 이용한 반사관계 확인
def is_reflecive(matrix):
    for i in range(len(matrix)):
        if matrix[i][i] != 1:
            return False
    return True

#==========================================================

#대칭관계

def is_symmetric(matrix):
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            if matrix[i][j] != matrix[j][i]:
                return False
    return True

#=========================================================

#추이 -> 거듭연산

    # R^2 계산
def matrix_square(matrix):
    n= len(matrix)
    R2 = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            for k in range(n):
                if matrix[i][k] == 1 and matrix[k][j] == 1:
                    R2[i][j] = 1
                    break
    return R2

    #R2 가 R의 부분집합인지 판단
def is_transitive(matrix):
    n = len(matrix)
    R2 = matrix_square(matrix)

    for i in range(n):
        for j in range(n):
            if R2[i][j] == 1 and matrix[i][j] == 0:
                return False
    return True


#========================================================

#추이 -> warshall

def warshall_closure(matrix):
    n = len(matrix)

    # 와샬 알고리즘 수행
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if matrix[i][j] == 0 and matrix[i][k] == 1 and matrix[k][j] == 1:
                    matrix[i][j] = 1

    return matrix
















