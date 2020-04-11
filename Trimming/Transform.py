import cv2
import numpy


def transform_by4(img, points):
	""" 4点を指定してトリミングする。 """

	points = sorted(points, key=lambda x:x[1])  # yが小さいもの順に並び替え。
	top = sorted(points[:2], key=lambda x:x[0])  # 前半二つは四角形の上。xで並び替えると左右も分かる。
	bottom = sorted(points[2:], key=lambda x:x[0], reverse=True)  # 後半二つは四角形の下。同じくxで並び替え。
	points = numpy.array(top + bottom, dtype='float32')  # 分離した二つを再結合。

	width = max(
        numpy.sqrt(
        (
            (points[0][0]-points[2][0])
            **2)
            *2),
            numpy.sqrt(
                (
                    (points[1][0]-points[3][0])
                    **2)
                    *2)
                    )
	height = max(
        numpy.sqrt(
            (
                (points[0][1]-points[2][1])
                **2)
                *2),
                numpy.sqrt(
                    (
                        (points[1][1]-points[3][1])
                        **2)
                        *2)
                        )

	dst = numpy.array([
			numpy.array([0, 0]),
			numpy.array([width-1, 0]),
			numpy.array([width-1, height-1]),
			numpy.array([0, height-1]),
			], numpy.float32)

	trans = cv2.getPerspectiveTransform(points, dst)  # 変換前の座標と変換後の座標の対応を渡すと、透視変換行列を作ってくれる。
	return cv2.warpPerspective(img, trans, (int(width), int(height)))  # 透視変換行列を使って切り抜く。