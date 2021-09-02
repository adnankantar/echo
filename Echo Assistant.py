from echo_functions import *

load_dotenv()
key = os.getenv("key")

with open('voice_id.txt', "r") as myfile:
    voice_id = int(myfile.read())
    myfile.close()

while True:
    flag, text = listen()
    label,confidence = check(text, key)
    answer(label,confidence,flag,voice_id)