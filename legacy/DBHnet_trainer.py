# 此模块用于yolov8n-cls分来模型的迁移训练

from ultralytics import YOLO
import torch

class DBHnettrainer:
    def __init__(self, model_path='assets/yolov8n-cls.pt'):
        # 加载预训练的YOLO-cls模型
        self.model = YOLO(model_path)

    def train_model(self, 
                    data_train_path, 
                    epochs=50, 
                    batch_size=16, 
                    img_size=224, 
                    device=0 if torch.cuda.is_available() else 'cpu',
                    project='DBHnet_project',
                    workers=4):
        # 迁移训练模型
        self.model.train(data=data_train_path, 
                         epochs=epochs,
                         batch=batch_size,
                         imgsz=img_size,
                         device=device,
                         project=project,
                         workers=workers)

# Example usage
if __name__ == "__main__":
    trainer = DBHnettrainer()
    data_train_path = 'DBHnet_data/train'  # 训练数据配置文件路径

    trainer.train_model(data_train_path)
    print("Model training completed.")