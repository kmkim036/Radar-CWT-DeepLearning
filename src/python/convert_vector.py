import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 경로
path = "/content/drive/MyDrive/data/"

date = 211118
whole_counts = 100


def preprocessing():                       # 함수 정의
    label = []
    image = np.zeros(shape=(whole_counts, 21, 101))  # 빈 넘파이형태 (21*101 형태로 설정)
    i = 0
    for person in range(0, 3):
        for motion in range(0, 4):
            cwt_data = pd.read_csv(path + date + "_" +
                                   person + "_" + motion + "_cwt.csv")
            for row in enumerate(cwt_data.index):
                # 공백으로 구분된 데이터를 넘파이로 변경
                df = np.fromstring(cwt_data['pixels'][row], dtype=int, sep=' ')
                df = np.reshape(df, (21, 101))
                image[i] = df
                label[i] = person * 4 + motion
                i = i + 1
    return image, label


# 데이터 불러오기
# cwt_data = pd.read_csv(path + "csv_data.csv")
# cwt_data['pixels']  # 데이터 구조 확인

if __name__ == "__main__":
    # preprocessing
    x_result, x_label = preprocessing()

    # check the preprocessed data
    x_result   # 전체 구조확인
    x_result[0]        # 0번째 값 확인
    plt.imshow(x_result[0])  # 0번째 값 출력