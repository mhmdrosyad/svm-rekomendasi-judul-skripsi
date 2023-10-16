import numpy as np
from sklearn.model_selection import train_test_split

def read_csv(file_path):
    data = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines[1:]:
            data.append(line.strip().split(','))
    return data

def select_atribute(data_array):
    data = []
    for row in data_array:
        data.append(row[3:7])
    return data

def select_label(data_array):
    data = []
    for row in data_array:
        data.append(row[-1])
    return data

#baca data dan ubah jadi array
data = read_csv('DATA_MHS_FINAL.csv')

#seleksi atribut dan memecah jadi 2 bagian (atribut dan label)
dataX = select_atribute(data)
dataY = select_label(data)

#ubah ke np array dan convert ke integer
array_X = np.array(dataX).astype(int)
array_Y = np.array(dataY).astype(int)

#pecah data menjadi data training dan data testing (80:20)
X_train,X_test,Y_train,Y_test = train_test_split(array_X,array_Y, test_size=0.2,stratify=array_Y,random_state=2)

#cek banyaknya data (muncul di terminal)
# print(array_X.shape,X_train.shape,X_test.shape)

X = X_train
Y = Y_train

# Inisialisasi bobot (a) dan bias (b)
a = np.zeros(X.shape[0])
b = 0

# Parameter pembelajaran
C = 1

# Menghitung matriks Hessian dengan kernel linear
Hessian = np.zeros((X.shape[0], X.shape[0]))
for i in range(X.shape[0]):
    for j in range(X.shape[0]):
        Hessian[i][j] = Y[i] * Y[j] * np.dot(X[i], X[j])

# Proses pelatihan SVM dengan kernel linear
for epoch in range(100):
    for i in range(X.shape[0]):
        Ei = np.dot(a * Y, Hessian[i]) + b - Y[i]
        if (Y[i] * Ei < -0.01 and a[i] < C) or (Y[i] * Ei > 0.01 and a[i] > 0):
            # Pilih indeks acak j yang berbeda dengan i
            j = i
            while j == i:
                j = np.random.randint(0, X.shape[0])

            Ej = np.dot(a * Y, Hessian[j]) + b - Y[j]

            # Simpan nilai lama
            ai_old, aj_old = a[i], a[j]
            bi_old, bj_old = b, b

            # Hitung batas atas (H) dan batas bawah (L)
            if Y[i] != Y[j]:
                L = max(0, aj_old - ai_old)
                H = min(C, C + aj_old - ai_old)
            else:
                L = max(0, ai_old + aj_old - C)
                H = min(C, ai_old + aj_old)

            if L == H:
                continue

            # Hitung nilai baru untuk aj
            aj_new = aj_old - Y[j] * (Ei - Ej)
            aj_new = max(L, min(H, aj_new))

            if np.abs(aj_new - aj_old) < 0.00001:
                continue

            # Hitung nilai baru untuk ai
            ai_new = ai_old + Y[i] * Y[j] * (aj_old - aj_new)

            # Hitung b
            bi_new = b - Ei - Y[i] * (ai_new - ai_old) * np.dot(X[i], X[i]) - Y[j] * (aj_new - aj_old) * np.dot(X[i], X[j])
            bj_new = b - Ej - Y[i] * (ai_new - ai_old) * np.dot(X[i], X[j]) - Y[j] * (aj_new - aj_old) * np.dot(X[j], X[j])

            if 0 < ai_new < C:
                b = bi_new
            elif 0 < aj_new < C:
                b = bj_new
            else:
                b = (bi_new + bj_new) / 2

            # Update nilai a
            a[i] = ai_new
            a[j] = aj_new


# Data uji
# X_test = np.array([
#     [77, 75, 70, 75],
#     [70, 86, 70, 70],
#     [85, 0, 85,	0]
# ])

# Melakukan prediksi dengan data uji
# predictions = []
# for i in range(X_test.shape[0]):
#     f_x = np.dot(a * Y, np.array([rbf_kernel(X[j], X_test[i]) for j in range(X.shape[0])])) + b
#     if f_x > 0:
#         predictions.append(1)
#     else:
#         predictions.append(-1)
# return predictions

#function prediksinya
def predict_with_svm(X_train, Y_train, X_test, a, b):
    predictions = []
    for i in range(X_test.shape[0]):
        f_x = np.dot(a * Y_train, np.array([np.dot(X_train[j], X_test[i]) for j in range(X_train.shape[0])])) + b
        if f_x > 0:
            predictions.append(1)
        else:
            predictions.append(-1)
    return predictions


# Menampilkan hasil prediksi
# print("Hasil Prediksi:", predictions)


predictions = predict_with_svm(X_train, Y_train, X_test, a, b)

#ubah hasik prediksi ke array np
Y_result = np.array(predictions)

#hitung jumlah data benar
jumlah_benar = np.sum(Y_test == Y_result)
jumlah_data = len(Y_test)

#cek akurasi data testing
akurasi = (jumlah_benar / jumlah_data) * 100

#cetak
print("Akurasi menggunakan data test: {:.2f}%".format(akurasi))

#kategori

kategori = {1: 'DATA MINING', -1: 'RPL'}

#data uji user
input_user = np.array([[85, 0, 85, 0]])

prediksi_user = predict_with_svm(X_train, Y_train, input_user, a, b)
hasil_prediksi = kategori.get(prediksi_user[0])

print(f"Hasil prediksi user: {hasil_prediksi}")