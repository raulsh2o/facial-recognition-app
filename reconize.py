import cv2
import face_recognition
image_count = 0

def main(args):
    image = cv2.imread("images/image.jpg")
    face_loc = face_recognition.face_locations(image)[0]
    face_image_encodings = face_recognition.face_encodings(image, known_face_locations=[face_loc])[0]
    
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    #cap = cv2.VideoCapture('rtsp://administrador:administrador@192.168.18.117:554/stream1') #IP Camera
    
    global image_count
    while True:
        ret, frame = cap.read()
        frame=cv2.resize(frame, (960, 540)) 
        if ret == False: break
        frame = cv2.flip(frame, 1)
        
        face_locations = face_recognition.face_locations(frame)
        if face_locations != []:
            for face_location in face_locations:
                face_frame_encodings = face_recognition.face_encodings(frame, known_face_locations=[face_location])[0]
                result = face_recognition.compare_faces([face_frame_encodings], face_image_encodings)
                if result[0] == True:
                    text = "Raul"
                    color = (125,220,0)
                else:
                    text = "Desconocido"
                    color = (50,50,255)
                    # Recortar la región de la cara
                    top, right, bottom, left = face_location
                    face_image = frame[top:bottom, left:right]

                    # Guardar la imagen de la cara
                    image_count += 1
                    image_filename = f"images/unknown_{image_count}.jpg"
                    cv2.imwrite(image_filename, face_image)
                    
                cv2.rectangle(frame, (face_location[3], face_location[2]), (face_location[1], face_location[2] + 30), color, -1)
                cv2.rectangle(frame, (face_location[3], face_location[0]), (face_location[1], face_location[2]), color, 2)
                cv2.putText(frame, text, (face_location[3], face_location[2]+20), 2, 0.7, (255,255,255), 1)
        cv2.imshow("Frame", frame)
        k = cv2.waitKey(1)
        if k == 27 & 0xFF:
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))