#encoding=utf-8
import speech_recognition as sr
import time

r = sr.Recognizer()
m = sr.Microphone()

try:
    print("A moment of silence, please...")
    with m as source: r.adjust_for_ambient_noise(source)
    print("Set minimum energy threshold to {}".format(r.energy_threshold))
    while True:
        print("Please say something: ")
        with m as source: audio = r.listen(source)
        try:
            # recognize speech using Google Speech Recognition
            begin_time = time.time()
            baidu_value = r.recognize_baidu(audio)
            end_time = time.time()
            print("Baidu result: {}".format(baidu_value))
            print("Baidu recognition time: {}s".format(end_time-begin_time))

            begin_time = time.time()
            sphinx_value = r.recognize_sphinx(audio)
            end_time =time.time()
            print("Sphinx result: {}".format(sphinx_value))
            print("Sphinx recognition time: {}s".format(end_time-begin_time))

        except sr.UnknownValueError:
            print("Oops! Didn't catch that")
        except sr.RequestError as e:
            print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
except KeyboardInterrupt:
    pass
    '''
