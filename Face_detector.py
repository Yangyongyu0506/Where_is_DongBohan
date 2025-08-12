# 此模块用于检测照片中的人脸并提取出来

import cv2
import os
from ultralytics import YOLO

class FaceDetector:
    def __init__(self, model_path='assets/human_face_detection.pt'): # 这里需要一个专门用于人脸检测的YOLO模型
        # 加载YOLO模型
        self.__model_detect = YOLO(model_path)

    def detect_faces(self, image_path):
        # 读取图像
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Image not found at {image_path}")

        # 使用YOLO模型进行人脸检测
        results = self.__model_detect(image)

        # 提取检测到的人脸区域
        faces = []
        coords = []
        for result in results:
            for box in result.boxes.xyxy:  # 获取边界框坐标
                x1, y1, x2, y2 = map(int, box)
                face = image[y1:y2, x1:x2]
                faces.append(face)
                coords.append((x1, y1, x2, y2))
        del(image)  # 清理内存
        return faces, coords

    def save_faces(self, faces, output_dir='output_faces'):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # 获取当前目录下所有face_*.jpg的最大编号
        existing = [f for f in os.listdir(output_dir) if f.startswith('face_') and f.endswith('.jpg')]
        max_idx = -1
        for fname in existing:
            try:
                idx = int(fname[len('face_'):-len('.jpg')])
                if idx > max_idx:
                    max_idx = idx
            except Exception:
                continue
        start_idx = max_idx + 1

        try:
            for i, face in enumerate(faces):
                face_path = os.path.join(output_dir, f'face_{start_idx + i}.jpg')
                face = cv2.resize(face, (224, 224))  # 可选：调整大小以适应模型输入
                # 保存人脸图像
                cv2.imwrite(face_path, face)
                print(f'Saved face {i} to {face_path}')
        except Exception as e:
            print(f"Error saving faces: {e}")
        del(faces)

# Example usage
if __name__ == "__main__":
    image_path = 'data_raw(from_wechat)/000.jpg'  # 示例图片路径
    mydetector = FaceDetector()
    faces, _ = mydetector.detect_faces(image_path)
    cv2.imshow('',faces[0])
    cv2.waitKey(0)
    # mydetector.save_faces(faces)