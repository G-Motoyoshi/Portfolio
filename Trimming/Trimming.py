import numpy as np
import tkinter
import datetime
import cv2
import Transform
from GUIc import fileopen, notice_end


# 画像の読み込み

filepath = fileopen('画像のファイルを選択してください。')
orig = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)

# 元画像のサイズを取得
o_width, o_height = orig.shape
o_square = o_width * o_height

# 輪郭を抽出する
for kernel_num in range(1,16,2): # 1<= x <= 15 の奇数
    gauss = cv2.GaussianBlur(orig, (kernel_num, kernel_num), 0)
    canny = cv2.Canny(gauss, 50, 100)

    kernel = np.ones((3, 20), np.uint8)
    closing = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel)

    kernel = np.ones((3, 3), np.uint8)
    dilation = cv2.dilate(closing, kernel, iterations = 1)
    erosion = cv2.erode(dilation, kernel, iterations = 1)

    cnts = cv2.findContours(erosion, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[1]  # 抽出した輪郭に近似する直線（？）を探す。
    cnts.sort(key=cv2.contourArea, reverse=True)  # 面積が大きい順に並べ替える。

    warp = None
    for cnt in cnts:
        arclen = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02*arclen, True)

        if len(approx) == 4:
            if warp is None:
                warp = approx.copy()  # 一番面積の大きな四角形をwarpに保存。

    if warp is not None:
        warped = Transform.transform_by4(gauss, warp[:,0,:])  # warpが存在した場合、そこだけくり抜いたものを作る。

#     切り出した画像のサイズを取得
    warped_w, warped_h = warped.shape
    w_square = warped_w * warped_h
# 切り出した画像が十分に大きければループを抜ける
    success_flag = False
    if 0.3 < w_square / o_square:
        now = datetime.datetime.now()
        cv2.imwrite(f'/Users/yamashitagenki/Downloads/Forte:Python/Portfolio/trimmings/trimming{now}.jpg', warped)
        success_flag = True
        break

if success_flag:
    notice_end('トリミングが完了しました。')
else:
    notice_end('トリミングに失敗しました。\n画像を変更してやり直してください。')
