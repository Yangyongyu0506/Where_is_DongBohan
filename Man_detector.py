# 此模块用于从图片中提取人脸，将人脸进行分类并找出目标人物，将认为是目标人物的人脸在原图片上框出来

from Face_detector import FaceDetector
from Face_classifier import FaceClassifier
from cv2 import rectangle, namedWindow, imshow, waitKey, destroyAllWindows, imread, WINDOW_NORMAL
from os.path import getctime

class ManDetector(FaceDetector, FaceClassifier):
    __slots__ = ('__model_detect_path', '__model_cls_path', 'expectation')

    def __init__(self, model_detect_path = 'assets/human_face_detection.pt', 
                 model_cls_path = 'assets/dbh_cls.pt',
                 expectation = 'DongBoHan'):
        """
        model_detect_path: str|None, path to the face detection yolo model
        model_cls_path: str|None, path to the face classification yolo-cls model
        expectation: str|None, the expected classification result
        """
        FaceDetector.__init__(self, model_detect_path)
        FaceClassifier.__init__(self, model_cls_path)
        self.expectation = expectation

    def detect_and_classify(self, image_path):
        """
        image_path: str, path to the input image
        """
        faces, coords = self.detect_faces(image_path)
        classified_faces = []
        for i, face in enumerate(faces):
            classification_result = self.classify_faces(face)
            if classification_result == self.expectation:
                classified_faces.append((face, coords[i]))
        return classified_faces

    def annotate_target(self, image_path):
        image = imread(image_path)
        time_img = getctime(image_path)
        for _, (x1, y1, x2, y2) in self.detect_and_classify(image_path):
            rectangle(image, (x1, y1), (x2, y2), (0, 0, 0), 3)
        namedWindow(wtitle := 'Annotated Image', WINDOW_NORMAL)
        imshow(wtitle, image)
        waitKey(0)
        destroyAllWindows()
        return image, time_img

    def __call__(self, image_path):
        image = imread(image_path)
        time_img = getctime(image_path)
        for _, (x1, y1, x2, y2) in self.detect_and_classify(image_path):
            rectangle(image, (x1, y1), (x2, y2), (0, 0, 0), 3)
        return image, time_img

# Example usage
if __name__ == "__main__":
    image_path = 'assets/data_raw(from_wechat)/000.jpg'  # 示例图片路径
    mydetector = ManDetector()
    mydetector.annotate_target(image_path)