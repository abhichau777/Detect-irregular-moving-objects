from tkinter import *
import cv2


top = Tk()
top.title("Irregular motion detector")
top.geometry("1080x720")


def fun():
    cap = cv2.VideoCapture(0)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
    out = cv2.VideoWriter("output.mp4", fourcc, 5.0, (1280, 720))
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()
    print(frame1.shape)


    while True:
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


        for contour in contours:

            (x1, y1, w, h) = cv2.boundingRect(contour)
            if cv2.contourArea(contour) < 900:
                continue
            cv2.rectangle(frame1, (x1, y1), (x1 + w, y1 + h), (0, 255, 0), 2)
            cv2.putText(frame1, "Status: {}".format('Irregular motion'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 0, 255), 1)
            approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
            cv2.drawContours(frame1, [approx], 0, (0, 0, 0), 1)
            x = approx.ravel()[0]
            y = approx.ravel()[1] - 5

            if len(approx) == 3:
                cv2.putText(frame1, "Triangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
            elif len(approx) == 4:
                x1, y1, w, h = cv2.boundingRect(approx)
                aspectRatio = float(w) / h
                print(aspectRatio)

                if aspectRatio >= 0.95 and aspectRatio <= 1.05:
                    cv2.putText(frame1, "square", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
                else:
                    cv2.putText(frame1, "rectangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))

            elif len(approx) == 5:
                cv2.putText(frame1, "Pentagon", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))

            elif len(approx) == 10:
                cv2.putText(frame1, "Star", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))

            else:
                cv2.putText(frame1, "Irregular Shape or Circle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))


        image = cv2.resize(frame1, (1280, 720))
        out.write(image)
        cv2.imshow("feed", frame1)
        frame1 = frame2
        ret, frame2 = cap.read()

        k = cv2.waitKey(1)

        if k == ord('q'):
            break

    cv2.destroyAllWindows()
    cap.release()
    out.release()



uname = Label(top, text = "DETECT IRREGULAR MOVING OBJECT AND TRACKING BASED ON COLOUR AND SHAPE IN REAL-TIME SYSTEM").place(x = 250,y = 50)
uname3 = Label(top, text = "MADE FOR GRAPHIC ERA HILL UNIVERSITY 4TH SEM MINI-PROJECT").place(x = 250,y = 100)
b1 = Button(top, text="START THE PROGRAM", command=fun, activeforeground="red", activebackground="pink", pady=10)
uname2 = Label(top, text = "Created By Abhishek Chauhan").place(x = 600,y = 600)
b1.place(relx=0.5, rely=0.5, anchor=CENTER)

top.mainloop()  
