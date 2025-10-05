# ==========================================
# 행렬 출력 (가독성 있는 테두리)
# ==========================================
def print_matrix(mx, colw=7, precision=3):
    fmt = f"{{:{colw}.{precision}f}}"
    row_strs = [" ".join(fmt.format(x) for x in row) for row in mx]
    inner_width = len(row_strs[0]) + 2
    print("┌" + "─" * inner_width + "┐")
    for s in row_strs:
        print(f"| {s} |")
    print("└" + "─" * inner_width + "┘")


# ==========================================
# [A | I] 형태로 증강행렬 출력
# ==========================================
def print_augmented(A, B, colw=7, precision=3):
    fmt = f"{{:{colw}.{precision}f}}"
    rows = []
    for i in range(len(A)):
        left = " ".join(fmt.format(x) for x in A[i])
        right = " ".join(fmt.format(x) for x in B[i])
        rows.append(f"{left} │ {right}")
    inner_width = len(rows[0]) + 2
    print("┌" + "─" * inner_width + "┐")
    for s in rows:
        print(f"| {s} |")
    print("└" + "─" * inner_width + "┘")


# ==========================================
# 전치행렬 / 소행렬 / 행렬식 / 역행렬(행렬식 이용)
# ==========================================
def transpose(m):
    return [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]

def minor_matrix(m, i, j):
    return [row[:j] + row[j+1:] for row in (m[:i] + m[i+1:])]

def determinant(m):
    if len(m) == 1:
        return m[0][0]
    if len(m) == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]
    det = 0
    for c in range(len(m)):
        det += ((-1) ** c) * m[0][c] * determinant(minor_matrix(m, 0, c))
    return det

def check_invertible(m):
    det = determinant(m)
    if abs(det) < 1e-10:
        print("이 행렬은 역행렬이 존재하지 않습니다. (det = 0)")
        return False
    return True

def inverse_by_determinant(m):
    det = determinant(m)
    if len(m) == 1:
        return [[1.0 / m[0][0]]]
    if len(m) == 2:
        return [[m[1][1] / det, -m[0][1] / det],
                [-m[1][0] / det,  m[0][0] / det]]
    cofactors = []
    for r in range(len(m)):
        row = []
        for c in range(len(m)):
            minor = minor_matrix(m, r, c)
            row.append(((-1) ** (r + c)) * determinant(minor))
        cofactors.append(row)
    adj = transpose(cofactors)
    for r in range(len(adj)):
        for c in range(len(adj)):
            adj[r][c] /= det
    return adj


# ==========================================
# 작은 값을 0으로 정리 (보기 좋게)
# ==========================================
def clean_small_values(M, eps=1e-12):
    for i in range(len(M)):
        for j in range(len(M[0])):
            if abs(M[i][j]) < eps:
                M[i][j] = 0.0


# ==========================================
# 가우스-조던 소거법 (단계별 시각화 포함)
# ==========================================
def inverse_by_gauss_jordan_steps(matrix, eps=1e-12):
    n = len(matrix)
    A = [row[:] for row in matrix]
    I = [[float(i == j) for j in range(n)] for i in range(n)]

    print("\n[초기 증강행렬  A | I ]")
    print_augmented(A, I)

    for i in range(n):
        print(f"\n=== 단계 {i+1}/{n} : 열 {i} 처리 ===")

        # 1) 기준 원소(pivot) 선택
        pivot_row = i
        if abs(A[pivot_row][i]) < eps:
            for r in range(i+1, n):
                if abs(A[r][i]) > eps:
                    pivot_row = r
                    break
        if abs(A[pivot_row][i]) < eps:
            raise ValueError("역행렬이 존재하지 않습니다. (피벗 0)")

        # 2) 행 교환
        if pivot_row != i:
            print(f"[행 교환] R{i} ↔ R{pivot_row}")
            A[i], A[pivot_row] = A[pivot_row], A[i]
            I[i], I[pivot_row] = I[pivot_row], I[i]
            clean_small_values(A, eps)
            clean_small_values(I, eps)
            print_augmented(A, I)

        # 3) 단위 행 변환
        pivot = A[i][i]
        print(f"[단위 행 변환] R{i} ← R{i} / {pivot:.6g}")
        for j in range(n):
            A[i][j] /= pivot
            I[i][j] /= pivot
        clean_small_values(A, eps)
        clean_small_values(I, eps)
        print_augmented(A, I)

        # 4) 나머지 행에서 해당 열 제거
        for r in range(n):
            if r == i:
                continue
            factor = A[r][i]
            if abs(factor) > eps:
                print(f"[행 소거] R{r} ← R{r} - ({factor:.6g})·R{i}")
                for j in range(n):
                    A[r][j] -= factor * A[i][j]
                    I[r][j] -= factor * I[i][j]
                clean_small_values(A, eps)
                clean_small_values(I, eps)
                print_augmented(A, I)

    print("\n[최종 결과  I | A⁻¹ ]")
    print_augmented(A, I)
    return I


# ==========================================
# (옵션) 단계 출력 없이 계산만 하는 버전
# ==========================================
def inverse_by_gauss_jordan(matrix, eps=1e-12):
    n = len(matrix)
    A = [row[:] for row in matrix]
    I = [[float(i == j) for j in range(n)] for i in range(n)]
    for i in range(n):
        pivot_row = i
        if abs(A[pivot_row][i]) < eps:
            for r in range(i+1, n):
                if abs(A[r][i]) > eps:
                    pivot_row = r
                    break
        if abs(A[pivot_row][i]) < eps:
            raise ValueError("역행렬이 존재하지 않습니다. (피벗 0)")
        if pivot_row != i:
            A[i], A[pivot_row] = A[pivot_row], A[i]
            I[i], I[pivot_row] = I[pivot_row], I[i]
        pivot = A[i][i]
        for j in range(n):
            A[i][j] /= pivot
            I[i][j] /= pivot
        for r in range(n):
            if r == i:
                continue
            factor = A[r][i]
            if abs(factor) > eps:
                for j in range(n):
                    A[r][j] -= factor * A[i][j]
                    I[r][j] -= factor * I[i][j]
    return I


# ==========================================
# 메인 실행부
# ==========================================
def main():
    try:
        n = int(input("정방행렬의 차수를 입력하세요: "))
        if n <= 0:
            print("차수는 양의 정수여야 합니다.")
            return

        print(f"{n}x{n} 행렬 A를 입력하세요 (한 행씩 공백으로 구분):")
        A = []
        for i in range(n):
            row = list(map(float, input(f"{i+1}행: ").split()))
            if len(row) != n:
                print("입력 오류: 정확히", n, "개의 숫자를 입력하세요.")
                return
            A.append(row)

        print("\n입력한 행렬 A:")
        print_matrix(A)

        if not check_invertible(A):
            return

        inv_det = inverse_by_determinant(A)
        print("\n[행렬식 이용 역행렬]")
        print_matrix(inv_det)

        show = input("\n가우스-조던 과정을 단계별로 볼까요? (y/n): ").strip().lower()
        if show == "y":
            inv_gj = inverse_by_gauss_jordan_steps(A)
        else:
            inv_gj = inverse_by_gauss_jordan(A)

        print("\n[가우스-조던 소거법 이용 역행렬]")
        print_matrix(inv_gj)

        same = all(abs(inv_det[i][j] - inv_gj[i][j]) < 1e-6 for i in range(n) for j in range(n))
        print("\n[결과 비교]")
        print("두 방법의 결과가 같습니다." if same else "두 방법의 결과가 약간 다릅니다.")

    except ValueError:
        print("입력 오류: 숫자를 입력해주세요.")
    except Exception as e:
        print("예상치 못한 오류 발생:", e)


if __name__ == "__main__":
    main()
