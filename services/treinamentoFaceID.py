import cv2
from sklearn.datasets import fetch_olivetti_faces

def treinamento():
    eigenface = cv2.face.EigenFaceRecognizer_create()

    faces= fetch_olivetti_faces(data_home= "assets/cv2/modelo/dataset")
    
    eigenface.train(faces.images, (faces.target * -1) - 1)
    eigenface.write('assets/cv2/modelo/classificadorEigen.yml')