import sys


def inticMatrix(size):
    matrix = [[0] * (size + 1) for _ in range(size)]
    for i in range(size):
        for j in range(size):
            matrix[i][j] = int(input(f"Введите элемент [{i}][{j}]: "))
    return matrix


def init_vector(size):
    vector = [0] * size
    for i in range(size):
        vector[i] = int(input(f"Введите элемент [{i}]: "))
    return vector


def matrix_dop(matrix, size, b):
    for i in range(size):
        matrix[i][size] = b[i]


def GausMethod(matrix, size):
    for i in range(size):
        # поиск главного элемента
        maxi = abs(matrix[i][i])
        index_row = i

        for k in range(i + 1, size):
            if abs(matrix[k][i]) > maxi:
                maxi = abs(matrix[k][i])
                index_row = k
        matrix[i], matrix[index_row] = matrix[index_row], matrix[i]
        if matrix[i][i] == 0:
            print("Матрица вырождена: единственное решение отсутствует")
            sys.exit()

        pivot = matrix[i][i]
        for j in range(i, size + 1):
            matrix[i][j] /= pivot
        for k in range(i + 1, size):
            koef = matrix[k][i]
            for j in range(i, size + 1):
                matrix[k][j] -= matrix[i][j] * koef


def ObratGausMethod(matrix, size, a):
    for i in range(size - 1, -1, -1):
        a[i] = matrix[i][size]
        for j in range(i + 1, size):
            a[i] -= matrix[i][j] * a[j]


def Matrix_Vector(matrix, size, a):
    vector_new = [0] * size
    for i in range(size):
        for j in range(size):
            vector_new[i] += matrix[i][j] * a[j]
    return vector_new


def is_symmetric(matrix, size):
    for i in range(size):
        for j in range(i + 1, size):
            if matrix[i][j] != matrix[j][i]:
                return False
    return True


print("Введите размер: ")
size = int(input())      
matrix = inticMatrix(size)
b = init_vector(size)
print("Выберите способ: \n1.Метод Гаусса \n2.Метод LDL факторизации")
vybor = int(input())
match vybor:
    case 1:
        a = [0] * size  # Вектор X
        x = [0] * size  # Вектор X
        f = [0] * size  # Вектор невязки

        print("Изначальная матрица : ", matrix, "Вектор b: ", b)
        matrix_original = [row[:] for row in matrix]  # Исходная матрица

        matrix_dop(matrix, size, b)  # Дополнение матрицы с вектором b
        GausMethod(matrix, size)
        print("Промежуточный результат после прямого хода : ", matrix)

        ObratGausMethod(matrix, size, a)
        print("Вектор x приблиз = ", a)
        c = Matrix_Vector(matrix_original, size, a)
        # Получаем A*x приблиз
        for i in range(size):
            f[i] = c[i] - b[i]
        print("Вектор невязки F: ", f)
        print("Норма вектора невязки:", max(abs(value) for value in f))
        matrix_dop(matrix_original, size, c)
        GausMethod(matrix_original, size)
        print("Промежуточный результат после прямого хода : ", matrix_original)
        ObratGausMethod(matrix_original, size, x)
        print("Вектор x точное = ", x)

        error = max(abs(x[i] - a[i]) for i in range(size))
        norm_x = max(abs(value) for value in x)
        if norm_x != 0:
            print("Относительная максимальная погрешность:", error / norm_x)
        else:
            print("Норма решения равна нулю; относительная погрешность не определена")
    case 2:
        Matrix_L = [[0] * (size) for _ in range(size)]
        Matrix_D = [[0] * (size) for _ in range(size)]
        Matrix_L_t = [[0] * (size+1) for _ in range(size)]
        x = [0] * size
        y = [0] * size
        z = [0] * size
        if not is_symmetric(matrix, size):
            print("Не симметрична!!!")
            sys.exit()
        for j in range(size):
            Matrix_D[j][j] = matrix[j][j]

            for k in range(j):
                Matrix_D[j][j] -= (
                    Matrix_L[j][k] *
                    Matrix_L[j][k] *
                    Matrix_D[k][k]
                )
            if Matrix_D[j][j] == 0:
                print("LDL^T-факторизация невозможна")
                sys.exit()
    
            Matrix_L[j][j] = 1
    
            for i in range(j + 1, size):

                Matrix_L[i][j] = matrix[i][j]

                for k in range(j):
                    Matrix_L[i][j] -= (
                        Matrix_L[i][k] *
                        Matrix_L[j][k] *
                        Matrix_D[k][k]
                    )

                Matrix_L[i][j] /= Matrix_D[j][j]
        print("Матрица L: " ,Matrix_L)
        print("Матрица D: " ,Matrix_D)
        
        for i in range(size):
            for j in range(i + 1, size):
                Matrix_L_t[i][j] = Matrix_L[j][i]
            Matrix_L_t[i][i]=1
        print("Матрица L транспонированя: " ,Matrix_L_t)
        
        for i in range(size):
            y[i] = b[i]
            for j in range(i):
                y[i] -= Matrix_L[i][j] * y[j]
        print("y = ", y)
        
        for i in range(size):
            z[i]=y[i]/Matrix_D[i][i]
        print("z = ", z)
        matrix_dop(Matrix_L_t,size,z)
        ObratGausMethod(Matrix_L_t,size,x)
        print("x= ",x)