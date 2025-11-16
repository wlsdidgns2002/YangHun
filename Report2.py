A = [1, 2, 3, 4, 5]
N = len(A)

def read_matrix(n: int):
    print(f"{n}x{n} 관계 행렬을 입력하세요. (0 또는 1)")
    values = []
    while len(values) < n * n:
        line = input().strip()
        if not line:
            continue
        parts = line.split()
        try:
            nums = [int(x) for x in parts]
        except ValueError:
            continue
        for v in nums:
            if v not in (0, 1):
                nums = []
                break
        values.extend(nums)

    values = values[: n * n]

    mat = []
    idx = 0
    for _ in range(n):
        row = values[idx:idx + n]
        idx += n
        mat.append(row)
    return mat

def show_matrix(mat, title=None):
    if title:
        print(title)
    for row in mat:
        print(" ".join(str(x) for x in row))
    print()

def check_reflexive(R):
    n = len(R)
    for i in range(n):
        if R[i][i] != 1:
            return False
    return True

def check_symmetric(R):
    n = len(R)
    for i in range(n):
        for j in range(n):
            if R[i][j] != R[j][i]:
                return False
    return True

def check_transitive(R):
    n = len(R)
    for i in range(n):
        for k in range(n):
            if R[i][k] == 1:
                for j in range(n):
                    if R[k][j] == 1 and R[i][j] == 0:
                        return False
    return True

def is_equiv(R):
    return check_reflexive(R) and check_symmetric(R) and check_transitive(R)

def make_classes(R, elems):
    n = len(R)
    visited = [False] * n
    groups = []

    for i in range(n):
        if visited[i]:
            continue
        temp = []
        for j in range(n):
            if R[i][j] == 1 and R[j][i] == 1:
                temp.append(elems[j])
                visited[j] = True
        groups.append(temp)
    return groups

def show_classes(R, elems):
    groups = make_classes(R, elems)
    print("동치류:")
    for g in groups:
        print("{" + ", ".join(str(x) for x in g) + "}")
    print()

def add_reflexive(R):
    n = len(R)
    res = [row[:] for row in R]
    for i in range(n):
        res[i][i] = 1
    return res

def add_symmetric(R):
    n = len(R)
    res = [row[:] for row in R]
    for i in range(n):
        for j in range(n):
            if res[i][j] == 1:
                res[j][i] = 1
    return res

# 추이 폐포 (정의 기반 반복)
def add_transitive_iter(R):
    n = len(R)
    res = [row[:] for row in R]
    while True:
        changed = False
        for i in range(n):
            for k in range(n):
                if res[i][k] == 1:
                    for j in range(n):
                        if res[k][j] == 1 and res[i][j] == 0:
                            res[i][j] = 1
                            changed = True
        if not changed:
            break
    return res

# 추이 폐포 (Warshall)
def add_transitive_warshall(R):
    n = len(R)
    res = [row[:] for row in R]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if res[i][k] == 1 and res[k][j] == 1:
                    res[i][j] = 1
    return res

def check_all(R, name="관계"):
    print(f"=== {name} 성질 검사 ===")
    r = check_reflexive(R)
    s = check_symmetric(R)
    t = check_transitive(R)

    print(f"반사성: {'예' if r else '아니오'}")
    print(f"대칭성: {'예' if s else '아니오'}")
    print(f"추이성: {'예' if t else '아니오'}")

    if r and s and t:
        print("→ 동치 관계입니다.")
        show_classes(R, A)
    else:
        print("→ 동치 관계가 아닙니다.\n")

def main():
    R = read_matrix(N)
    show_matrix(R, "입력된 관계:")

    check_all(R, "입력 관계")

    R1 = add_reflexive(R)
    print("=== 반사 폐포 ===")
    show_matrix(R, "변환 전:")
    show_matrix(R1, "변환 후:")
    check_all(R1, "반사 폐포")

    R2 = add_symmetric(R)
    print("=== 대칭 폐포 ===")
    show_matrix(R, "변환 전:")
    show_matrix(R2, "변환 후:")
    check_all(R2, "대칭 폐포")

    print("=== 추이 폐포 ===")
    R3_iter = add_transitive_iter(R)
    R3_warshall = add_transitive_warshall(R)

    show_matrix(R, "변환 전:")
    show_matrix(R3_iter, "추이 폐포 (정의 기반 반복 방식):")
    show_matrix(R3_warshall, "추이 폐포 (Warshall 알고리즘):")

    check_all(R3_iter, "추이 폐포 (정의 기반 반복 방식)")

if __name__ == "__main__":
    main()
