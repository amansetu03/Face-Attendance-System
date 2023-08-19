import cv2
import face_recognition
import pickle
import os


class AutoEncoading:
    def __init__(self):
        self.studentIds = []
        self.PathList = os.listdir('Images')
        for path in self.PathList:
            self.studentIds.append(os.path.splitext(path)[0])

    def findEncodings(self,images):
        encodeList = []
        for imgPath in images:
            img = cv2.imread(f'Images/{imgPath}')
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # cv2.imshow("Face Attendance", gray_img)
            # cv2.waitKey(1)
            # cv2.destroyAllWindows()
            faceLocations = face_recognition.face_locations(gray_img)
            if len(faceLocations) > 0:
                encode = face_recognition.face_encodings(img, [faceLocations[0]])[0]
                encodeList.append(encode)
        return encodeList

    def getEncoading(self):
        print("Encoding Started ...")
        encodeListKnown = self.findEncodings(self.PathList)
        encodeListKnownWithIds = [encodeListKnown, self.studentIds]
        print("Encoding Complete")
        try:
            file = open("EncodeFile.p", 'wb')
            pickle.dump(encodeListKnownWithIds, file)
            file.close()
        except:
            print("there is an error while saving model.")
        print("File Saved")


Au = AutoEncoading()
Au.getEncoading()
