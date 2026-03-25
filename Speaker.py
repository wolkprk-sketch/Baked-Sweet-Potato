import pyttsx3
import time
class Speaker:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # Set speech rate
        self.engine.setProperty('volume', 1.0)  # Set volume (0.0 to 1.0)
    
    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()  # Process the speech events
        self.engine.startLoop(False)  # Start the event loop without blocking
        self.engine.iterate()  # Process the speech events
        self.engine.endLoop()  # End the event loop after speaking  
        
    def __exit__(self):
        self.engine.stop()


if __name__ == '__main__':
    speaker = Speaker()
    speaker.speak("Hello, this is a test of the speaker module.")
    speaker.speak("Goodbye")
