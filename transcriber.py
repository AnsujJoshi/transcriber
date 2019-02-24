'''Transcriber to convert speech to text'''
import speech_recognition as sr
import time


def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.
    
    recognizer : `Recognizer` instance of SpeechRecogination
    microphone : `Microphone` instance of SpeechRecogination

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


def write_files(data, file_name):
    '''Append data to the text

    Args:
        data : string, Data given to the function
        file_name : string, name of the file to be written
    '''
    t = time.localtime()
    header = '------ \n Date : {}/{}/{} \n Time : {}:{}:{} \n'.format(
        t.tm_mday, t.tm_mon, t.tm_year, t.tm_hour, t.tm_min, t.tm_sec
    )
    with open(file_name, 'a+') as file:
        file.write(header)
        file.write(data)

if __name__ == '__main__':

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print('SPEAK!!')

    while True:
        response = recognize_speech_from_mic(recognizer, microphone)
        print(response)
        if response['transcription'] is not None:
            write_files(response['transcription'], 'text.txt')
        else:
            break
