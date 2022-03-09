import tensorflow as tf
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from tensorflow.keras.callbacks import EarlyStopping
from keras.utils import np_utils
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns

import models

augment_ratio = 9

try_num = 10   # 같은 조건에서 몇번 반복할지

date = '220132'

count = 100

lr = 0.001
bs = 64
wsr = 0.15

classnum_human = 4
classnum_motion = 3

test_label_human = np.zeros(classnum_human).reshape(1, classnum_human)
predict_label_human = np.zeros(classnum_human).reshape(1, classnum_human)

test_label_motion = np.zeros(classnum_motion).reshape(1, classnum_motion)
predict_label_motion = np.zeros(classnum_motion).reshape(1, classnum_motion)


file_name = '_stft.txt'

start_row = 0
end_row = 128
scale_row = 1
rows = 128

start_col = 0
end_col = 29
scale_col = 1
cols = 29



def preprocessing(person, motion):  # person, motion에 해당하는 image 불러옴
    DirectoryPath = '/home/kmkim/Projects/git/kmkim036/Radar-STFT-DeepLearning/txt/'
    image = np.zeros(shape=(count, rows, cols, 1))
    label1 = []
    label2 = []

    cwt_data = pd.read_csv(
        DirectoryPath + date + "_" + str(person) + "_" + str(motion) + file_name)
    for i in range(0, 100):
        df = np.fromstring(cwt_data['pixels'][i], dtype=int, sep=' ')
        df = np.reshape(df, (rows, cols, 1))
        image[i] = df
        label1.append(person - 1)
        if motion == 0:
            label2.append(motion)
        else:
            label2.append(motion - 1)

    return image, label1, label2

# ratio비율로 각 data set을 합치고 순서도 섞음
def concatenate_n_div(image0, label0_1, label0_2, image1, label1_1, label1_2, image2, label2_1, label2_2, image3, label3_1, label3_2, image4, label4_1, label4_2, image5, label5_1, label5_2, image6, label6_1, label6_2, image7, label7_1, label7_2, image8, label8_1, label8_2, image9, label9_1, label9_2, image10, label10_1, label10_2, image11, label11_1, label11_2):
    train_ratio = 0.7
    val_ratio = 0.15
    test_ratio = 0.15  # 적용안됨

    x_train = np.concatenate(
        (image0[0:int(count*train_ratio)],
         image1[0:int(count*train_ratio)],
         image2[0:int(count*train_ratio)],
         image3[0:int(count*train_ratio)],
         image4[0:int(count*train_ratio)],
         image5[0:int(count*train_ratio)],
         image6[0:int(count*train_ratio)],
         image7[0:int(count*train_ratio)],
         image8[0:int(count*train_ratio)],
         image9[0:int(count*train_ratio)],
         image10[0:int(count*train_ratio)],
         image11[0:int(count*train_ratio)]))
    y_train_human = np.concatenate(
        (label0_1[0:int(count*train_ratio)],
         label1_1[0:int(count*train_ratio)],
         label2_1[0:int(count*train_ratio)],
         label3_1[0:int(count*train_ratio)],
         label4_1[0:int(count*train_ratio)],
         label5_1[0:int(count*train_ratio)],
         label6_1[0:int(count*train_ratio)],
         label7_1[0:int(count*train_ratio)],
         label8_1[0:int(count*train_ratio)],
         label9_1[0:int(count*train_ratio)],
         label10_1[0:int(count*train_ratio)],
         label11_1[0:int(count*train_ratio)]))
    y_train_motion = np.concatenate(
        (label0_2[0:int(count*train_ratio)],
         label1_2[0:int(count*train_ratio)],
         label2_2[0:int(count*train_ratio)],
         label3_2[0:int(count*train_ratio)],
         label4_2[0:int(count*train_ratio)],
         label5_2[0:int(count*train_ratio)],
         label6_2[0:int(count*train_ratio)],
         label7_2[0:int(count*train_ratio)],
         label8_2[0:int(count*train_ratio)],
         label9_2[0:int(count*train_ratio)],
         label10_2[0:int(count*train_ratio)],
         label11_2[0:int(count*train_ratio)]))
    x_val = np.concatenate((image0[int(count*train_ratio):int(count *
                                                              train_ratio + count*val_ratio)],
                            image1[int(count*train_ratio):int(count *
                                                              train_ratio + count*val_ratio)],
                            image2[int(count*train_ratio):int(count *
                                                              train_ratio + count*val_ratio)],
                            image3[int(count*train_ratio):int(count *
                                                              train_ratio + count*val_ratio)],
                            image4[int(count*train_ratio):int(count *
                                                              train_ratio + count*val_ratio)],
                            image5[int(count*train_ratio):int(count *
                                                              train_ratio + count*val_ratio)],
                            image6[int(count*train_ratio):int(count *
                                                              train_ratio + count*val_ratio)],
                            image7[int(count*train_ratio):int(count *
                                                              train_ratio + count*val_ratio)],
                            image8[int(count*train_ratio):int(count *
                                                              train_ratio + count*val_ratio)],
                            image9[int(count*train_ratio):int(count *
                                                              train_ratio + count*val_ratio)],
                            image10[int(count*train_ratio):int(count *
                                                               train_ratio + count*val_ratio)],
                            image11[int(count*train_ratio):int(count *
                                                               train_ratio + count*val_ratio)]))
    y_val_human = np.concatenate((label0_1[int(count*train_ratio):int(count*train_ratio + count*val_ratio)],
                                  label1_1[int(
                                      count*train_ratio):int(count*train_ratio + count*val_ratio)],
                                  label2_1[int(
                                      count*train_ratio):int(count*train_ratio + count*val_ratio)],
                                  label3_1[int(
                                      count*train_ratio):int(count*train_ratio + count*val_ratio)],
                                  label4_1[int(
                                      count*train_ratio):int(count*train_ratio + count*val_ratio)],
                                  label5_1[int(
                                      count*train_ratio):int(count*train_ratio + count*val_ratio)],
                                  label6_1[int(
                                      count*train_ratio):int(count*train_ratio + count*val_ratio)],
                                  label7_1[int(
                                      count*train_ratio):int(count*train_ratio + count*val_ratio)],
                                  label8_1[int(
                                      count*train_ratio):int(count*train_ratio + count*val_ratio)],
                                  label9_1[int(
                                      count*train_ratio):int(count*train_ratio + count*val_ratio)],
                                  label10_1[int(
                                      count*train_ratio):int(count*train_ratio + count*val_ratio)],
                                  label11_1[int(count*train_ratio):int(count*train_ratio + count*val_ratio)]))
    y_val_motion = np.concatenate((label0_2[int(count*train_ratio):int(count*train_ratio + count*val_ratio)],
                                   label1_2[int(
                                       count*train_ratio):int(count*train_ratio + count*val_ratio)],
                                   label2_2[int(
                                       count*train_ratio):int(count*train_ratio + count*val_ratio)],
                                   label3_2[int(
                                       count*train_ratio):int(count*train_ratio + count*val_ratio)],
                                   label4_2[int(
                                       count*train_ratio):int(count*train_ratio + count*val_ratio)],
                                   label5_2[int(
                                       count*train_ratio):int(count*train_ratio + count*val_ratio)],
                                   label6_2[int(
                                       count*train_ratio):int(count*train_ratio + count*val_ratio)],
                                   label7_2[int(
                                       count*train_ratio):int(count*train_ratio + count*val_ratio)],
                                   label8_2[int(
                                       count*train_ratio):int(count*train_ratio + count*val_ratio)],
                                   label9_2[int(
                                       count*train_ratio):int(count*train_ratio + count*val_ratio)],
                                   label10_2[int(
                                       count*train_ratio):int(count*train_ratio + count*val_ratio)],
                                   label11_2[int(count*train_ratio):int(count*train_ratio + count*val_ratio)]))
    x_test = np.concatenate((image0[int(count*train_ratio +
                                        count*val_ratio): count],
                             image1[int(count*train_ratio +
                                        count*val_ratio): count],
                             image2[int(count*train_ratio +
                                        count*val_ratio): count],
                             image3[int(count*train_ratio +
                                        count*val_ratio): count],
                             image4[int(count*train_ratio +
                                        count*val_ratio): count],
                             image5[int(count*train_ratio +
                                        count*val_ratio): count],
                             image6[int(count*train_ratio +
                                        count*val_ratio): count],
                             image7[int(count*train_ratio +
                                        count*val_ratio): count],
                             image8[int(count*train_ratio +
                                        count*val_ratio): count],
                             image9[int(count*train_ratio +
                                        count*val_ratio): count],
                             image10[int(count*train_ratio +
                                         count*val_ratio): count],
                             image11[int(count*train_ratio +
                                         count*val_ratio): count]))
    y_test_human = np.concatenate((label0_1[int(count*train_ratio + count*val_ratio): count],
                                   label1_1[int(
                                       count*train_ratio + count*val_ratio): count],
                                   label2_1[int(
                                       count*train_ratio + count*val_ratio): count],
                                   label3_1[int(
                                       count*train_ratio + count*val_ratio): count],
                                   label4_1[int(
                                       count*train_ratio + count*val_ratio): count],
                                   label5_1[int(
                                       count*train_ratio + count*val_ratio): count],
                                   label6_1[int(
                                       count*train_ratio + count*val_ratio): count],
                                   label7_1[int(
                                       count*train_ratio + count*val_ratio): count],
                                   label8_1[int(
                                       count*train_ratio + count*val_ratio): count],
                                   label9_1[int(
                                       count*train_ratio + count*val_ratio): count],
                                   label10_1[int(
                                       count*train_ratio + count*val_ratio): count],
                                   label11_1[int(count*train_ratio + count*val_ratio): count]))
    y_test_motion = np.concatenate((label0_2[int(count*train_ratio + count*val_ratio): count],
                                    label1_2[int(
                                        count*train_ratio + count*val_ratio): count],
                                    label2_2[int(
                                        count*train_ratio + count*val_ratio): count],
                                    label3_2[int(
                                        count*train_ratio + count*val_ratio): count],
                                    label4_2[int(
                                        count*train_ratio + count*val_ratio): count],
                                    label5_2[int(
                                        count*train_ratio + count*val_ratio): count],
                                    label6_2[int(
                                        count*train_ratio + count*val_ratio): count],
                                    label7_2[int(
                                        count*train_ratio + count*val_ratio): count],
                                    label8_2[int(
                                        count*train_ratio + count*val_ratio): count],
                                    label9_2[int(
                                        count*train_ratio + count*val_ratio): count],
                                    label10_2[int(
                                        count*train_ratio + count*val_ratio): count],
                                    label11_2[int(count*train_ratio + count*val_ratio): count]))

    train_gen = ImageDataGenerator(
        width_shift_range=wsr
    )
    augment_size = int(augment_ratio * x_train.shape[0])
    randidx = np.random.randint(x_train.shape[0], size=augment_size)
    x_augmented = x_train[randidx].copy()
    y_augmented_human = y_train_human[randidx].copy()
    y_augmented_motion = y_train_motion[randidx].copy()
    x_augmented, y_augmented_human = train_gen.flow(
        x_augmented, y_augmented_human, batch_size=augment_size, shuffle=False).next()
    x_augmented, y_augmented_motion = train_gen.flow(
        x_augmented, y_augmented_motion, batch_size=augment_size, shuffle=False).next()
    x_train = np.concatenate((x_train, x_augmented))
    y_train_human = np.concatenate((y_train_human, y_augmented_human))
    y_train_motion = np.concatenate((y_train_motion, y_augmented_motion))

    s = np.arange(x_train.shape[0])
    np.random.shuffle(s)
    x_train = x_train[s]
    y_train_human = y_train_human[s]
    y_train_motion = y_train_motion[s]

    s = np.arange(x_val.shape[0])
    np.random.shuffle(s)
    x_val = x_val[s]
    y_val_human = y_val_human[s]
    y_val_motion = y_val_motion[s]

    s = np.arange(x_test.shape[0])
    np.random.shuffle(s)
    x_test = x_test[s]
    y_test_human = y_test_human[s]
    y_test_motion = y_test_motion[s]

    return x_train, y_train_human, y_train_motion, x_val, y_val_human, y_val_motion, x_test, y_test_human, y_test_motion


row_len = math.ceil((end_row - start_row))
col_len = math.ceil((end_col - start_col))

image1, label1_1, label1_2 = preprocessing(1, 0)
image2, label2_1, label2_2 = preprocessing(1, 2)
image3, label3_1, label3_2 = preprocessing(1, 3)
image4, label4_1, label4_2 = preprocessing(2, 0)
image5, label5_1, label5_2 = preprocessing(2, 2)
image6, label6_1, label6_2 = preprocessing(2, 3)
image7, label7_1, label7_2 = preprocessing(3, 0)
image8, label8_1, label8_2 = preprocessing(3, 2)
image9, label9_1, label9_2 = preprocessing(3, 3)
image10, label10_1, label10_2 = preprocessing(4, 0)
image11, label11_1, label11_2 = preprocessing(4, 2)
image12, label12_1, label12_2 = preprocessing(4, 3)

result_acc_1 = 0
result_acc_2 = 0
for i in range(try_num):
    print(str(i + 1) + ' repeat')

    # 순서를 섞음
    s = np.arange(image1.shape[0])
    np.random.shuffle(s)
    image1_shuff = image1[s]

    s = np.arange(image2.shape[0])
    np.random.shuffle(s)
    image2_shuff = image2[s]

    s = np.arange(image3.shape[0])
    np.random.shuffle(s)
    image3_shuff = image3[s]

    s = np.arange(image4.shape[0])
    np.random.shuffle(s)
    image4_shuff = image4[s]

    s = np.arange(image5.shape[0])
    np.random.shuffle(s)
    image5_shuff = image5[s]

    s = np.arange(image6.shape[0])
    np.random.shuffle(s)
    image6_shuff = image6[s]

    s = np.arange(image7.shape[0])
    np.random.shuffle(s)
    image7_shuff = image7[s]

    s = np.arange(image8.shape[0])
    np.random.shuffle(s)
    image8_shuff = image8[s]

    s = np.arange(image9.shape[0])
    np.random.shuffle(s)
    image9_shuff = image9[s]

    s = np.arange(image10.shape[0])
    np.random.shuffle(s)
    image10_shuff = image10[s]

    s = np.arange(image11.shape[0])
    np.random.shuffle(s)
    image11_shuff = image11[s]

    s = np.arange(image12.shape[0])
    np.random.shuffle(s)
    image12_shuff = image12[s]

    # 자른 image를 각 data set으로 나눠서 합침
    x_train, y_train_human, y_train_motion, x_val, y_val_human, y_val_motion, x_test, y_test_human, y_test_motion = concatenate_n_div(
        image1_shuff, label1_1, label1_2, image2_shuff, label2_1, label2_2, image3_shuff, label3_1, label3_2, image4_shuff, label4_1, label4_2, image5_shuff, label5_1, label5_2, image6_shuff, label6_1, label6_2, image7_shuff, label7_1, label7_2, image8_shuff, label8_1, label8_2, image9_shuff, label9_1, label9_2, image10_shuff, label10_1, label10_2, image11_shuff, label11_1, label11_2, image12_shuff, label12_1, label12_2)

    maxval = x_train.max()
    if maxval < x_val.max():
        maxval = x_val.max()
    if maxval < x_test.max():
        maxval = x_test.max()

    # 정규화
    x_train = x_train.astype('float32')/maxval
    x_val = x_val.astype('float32')/maxval
    x_test = x_test.astype('float32')/maxval

    # CNN model
    model = models.create_CNNmodel_MTL(
        classnum_human, classnum_motion, lr, row_len, col_len)

    if i == 0:
        print(x_train.shape[0])
        print(x_val.shape[0])
        print(x_test.shape[0])
        print(model.summary())

    early_stopping = EarlyStopping(
        monitor='val_human_output_accuracy', patience=10)
    y_train_human = np_utils.to_categorical(y_train_human, classnum_human)
    y_train_motion = np_utils.to_categorical(y_train_motion, classnum_motion)
    y_val_human = np_utils.to_categorical(y_val_human, classnum_human)
    y_val_motion = np_utils.to_categorical(y_val_motion, classnum_motion)
    y_test_human = np_utils.to_categorical(y_test_human, classnum_human)
    y_test_motion = np_utils.to_categorical(y_test_motion, classnum_motion)
    hist = model.fit({'main_input': x_train}, {'human_output': y_train_human, 'motion_output': y_train_motion},
                     validation_data=(x_val, [y_val_human, y_val_motion]), epochs=50, verbose=0, callbacks=[early_stopping], batch_size=bs)

    # 평가
    # print('Evaluate')
    score = model.evaluate(x_test, [y_test_human, y_test_motion])
    result_acc_1 = result_acc_1 + score[3]    # 정확도 결과 저장하여 평균값 내는데 사용
    result_acc_2 = result_acc_2 + score[4]    # 정확도 결과 저장하여 평균값 내는데 사용

    test_label_human = np.concatenate((test_label_human, y_test_human))
    test_label_motion = np.concatenate((test_label_motion, y_test_motion))
    pred = model.predict(x_test)
    predict_label_human = np.concatenate((predict_label_human, pred[0]))
    predict_label_motion = np.concatenate((predict_label_motion, pred[1]))

print('image size :', str(row_len)+'X'+str(col_len), '   row =', str(start_row)+' : '+str(end_row), '   col =', str(start_col)+' : '+str(end_col),
      '   round :', try_num, '//  average_acc_human :', result_acc_1 / try_num, 'average_acc_motion :', result_acc_2 / try_num)

test_label_human = np.delete(test_label_human, 0, axis=0)
test_label_motion = np.delete(test_label_motion, 0, axis=0)
predict_label_human = np.delete(predict_label_human, 0, axis=0)
predict_label_motion = np.delete(predict_label_motion, 0, axis=0)

sns.set(style='white')
plt.figure(figsize=(classnum_human, classnum_human))
cm = confusion_matrix(np.argmax(test_label_human[:int(test_label_human.shape[0])], axis=1),
                      np.argmax(predict_label_human[:int(predict_label_human.shape[0])], axis=-1))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()

sns.set(style='white')
plt.figure(figsize=(classnum_motion, classnum_motion))
cm = confusion_matrix(np.argmax(test_label_motion[:int(test_label_motion.shape[0])], axis=1),
                      np.argmax(predict_label_motion[:int(predict_label_motion.shape[0])], axis=-1))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()