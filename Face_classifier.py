# 此程序用于对提取的人脸进行分类，找出哪些人脸是目标人物

from ultralytics import YOLO

class FaceClassifier:
    def __init__(self, model_path='assets/yolov8n-cls.pt'):
        # 加载预训练的YOLO-cls模型
        self.__model_cls = YOLO(model_path)
        
    def classify_faces(self, img_input):
        results = self.__model_cls(img_input)
        return results[0].names[results[0].probs.top1]

# Example usage
if __name__ == "__main__":
    # 示例用法
    classifier = FaceClassifier('assets/dbh_cls.pt')
    image_path = 'output_faces/face_0.jpg'  # 示例图像路径
    try:
        results = classifier.classify_faces(image_path)
        print("Classification results:", results)
    except Exception as e:
        print(f"Error during classification: {e}")
