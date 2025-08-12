# 此模块用于批量从图像文件中提取人脸并保存

import os
from Face_detector import FaceDetector
from tqdm import tqdm

class BatchFaceExtractor:
    def __init__(self, facedetector: FaceDetector):
        self.facedetector = facedetector

    def process_directory(self, input_dir, output_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        for image_file in tqdm(image_files, desc="Processing images"):
            image_path = os.path.join(input_dir, image_file)
            faces, _ = self.facedetector.detect_faces(image_path)
            self.facedetector.save_faces(faces, output_dir)
        del(image_files)  # 清理内存

# Example usage
if __name__ == "__main__":
    input_dir = 'data_raw(from_wechat)'  # 输入目录，包含待处理的图像
    output_dir = 'output_faces'  # 输出目录，用于保存提取的人脸图像

    mydetector = FaceDetector()
    batch_extractor = BatchFaceExtractor(mydetector)
    batch_extractor.process_directory(input_dir, output_dir)