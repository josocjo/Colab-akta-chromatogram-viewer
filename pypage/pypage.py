import cv2
import numpy as np
from scipy.signal import find_peaks
from scipy.ndimage import gaussian_filter1d

def detect_and_correct_tilt(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    lines = cv2.HoughLines(edges, 1, np.pi/180, 100)
    if lines is not None:
        for rho, theta in lines[0]:
            if np.pi/4 < theta < 3*np.pi/4:
                angle = theta - np.pi/2
                break
        else:
            angle = 0
    else:
        angle = 0

    center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(center, angle * 180 / np.pi, 1.0)

    # 回転後の画像サイズを計算
    cos = np.abs(rot_mat[0, 0])
    sin = np.abs(rot_mat[0, 1])
    new_w = int((image.shape[0] * sin) + (image.shape[1] * cos)) +50
    new_h = int((image.shape[0] * cos) + (image.shape[1] * sin))

    # 平行移動を調整
    rot_mat[0, 2] += (new_w / 2) - center[0]
    rot_mat[1, 2] += (new_h / 2) - center[1]

    # 白背景で回転
    return cv2.warpAffine(image, rot_mat, (new_w, new_h), borderValue=(255,255,255))

def detect_lanes(image, expected_lane_width=30):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # エッジ検出
    edges = get_edges(gray)

    # 垂直方向のエッジプロファイルを計算
    edge_profile = np.sum(edges, axis=0)

    # エッジプロファイルをスムージング
    smoothed_profile = gaussian_filter1d(edge_profile, sigma=5)

    # ピーク（エッジ）検出
    peaks, _ = find_peaks(255-smoothed_profile, distance=expected_lane_width*0.8, prominence=1,)

    # レーンの境界ペアを形成
    lane_boundaries = []
    for i in range(0, len(peaks) - 1, 2):
        if peaks[i+1] - peaks[i] < expected_lane_width * 1.5:
            lane_boundaries.append((peaks[i], peaks[i+1]))

    # レーンの中心を計算
    lane_centers = [(start + end) // 2 for start, end in lane_boundaries]

    # レーンの連続性を考慮した後処理
    final_lanes = []
    for i, center in enumerate(lane_centers):
        if i == 0 or abs(center - final_lanes[-1]) > expected_lane_width * 0.8:
            final_lanes.append(center)
        else:
            # 近接したレーンは平均化
            final_lanes[-1] = (final_lanes[-1] + center) // 2

    final_lanes =insert_mean(np.array(final_lanes),expected_lane_width,image.shape[1]).astype(int)

    return final_lanes


def get_edges(image):
  # ノイズ除去（メディアンフィルタ）
  image = cv2.medianBlur(image, 5)
  # Sobelフィルタを適用
  sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=5)               # 垂直方向の勾配

  # 勾配の絶対値を計算
  sobel_y = cv2.convertScaleAbs(sobel_y)
  return sobel_y

  

def insert_mean(arr,lane_width,maximum,minimum=0):
    """各数字の間に平均を挿入し、最小値と最大値まで平均差分で埋める"""
    n = len(arr)
    append_arr = []
    for i in range(n-1):
      if arr[i] + lane_width*1.1 > arr[i+1]:
        continue
      
      else:
        non_arr_n = (arr[i+1] - arr[i])//lane_width
        for k in range(non_arr_n-1):
          append_arr.append( arr[i] + k * (arr[i+1] - arr[i]) / non_arr_n)


    #if n <= 1:  # 1要素以下の配列の場合はそのまま返す
    #    return arr
    #means = (arr[:-1] + arr[1:]) / 2
    #new_arr = np.concatenate((arr, means)) # concatenateで連結
    new_arr = np.concatenate((arr, append_arr))
    new_arr = np.sort(new_arr)

    mean_size = np.mean(np.diff(new_arr))

    low_arr = np.arange(new_arr[0], minimum, -mean_size)
    high_arr = np.arange(new_arr[-1], maximum, mean_size)

    new_arr = np.concatenate((low_arr[1:], new_arr[:-1], high_arr))

    return np.sort(new_arr)

def draw_rectangles(image, lanes, lane_width=30):
    result = image.copy()
    height, width = image.shape[:2]
    for lane in lanes:
        cv2.rectangle(result, (int(lane-lane_width//2), 0), (int(lane+lane_width//2), height), random_color(), 2)
    return result

def process_cbb_image(image_path, expected_lane_width=50):
    image = cv2.imread(image_path)
    corrected_image = detect_and_correct_tilt(image)
    lanes = detect_lanes(corrected_image, expected_lane_width)
    result = draw_rectangles(corrected_image, lanes, expected_lane_width)
    return result

def random_color():
    return [int(c) for c in np.random.randint(0, 255, 3).astype(int)]