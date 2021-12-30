########################################################
# Solution Challenge of Insomnia404
# Author: Insomnia404
# Date: 12/30/2021
# All rights reserved

########################################################

########################################################
# Imports
import os
import zipfile
import re
import time
#import numpy as np
from PIL import Image, ImageChops
from pyzbar.pyzbar import decode
from tqdm import tqdm

########################################################

########################################################
# Challenge 1 Unzip Zip-Files
########################################################

def unzip_directory(directory):
    # This function unzips and then delete all zip files
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if re.search(r'\.txt$', file_name):
                print("Textfile be found")
                break
            if re.search(r'\.zip$', file_name):
                #zip_lastfile = file_name
                to_path = os.path.join(root, file_name.split('.zip')[0])
                zipped_file = os.path.join(root, file_name)
                if not os.path.exists(to_path):
                    os.makedirs(to_path)
                with zipfile.ZipFile(zipped_file, 'r') as zfile:
                    zfile.extractall(root)
                os.removedirs(to_path)
                time.sleep(1)
                os.remove(zfile.filename) #delete old zip-file
                # deletes zip file

def exists_zip(directory):
    # This function returns T/F whether any .zip file exist
    is_zip = False
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if re.search(r'\.zip$', file_name):
                is_zip = True
    return is_zip


def unzip_directory_recursively(directory, max_iter):
    print("Does the directory path exits?", os.path.exists(directory))
    iterate = 0

    while exists_zip(directory) or iterate < max_iter:
        unzip_directory(directory)
        iterate += 1

    pre = "Did not " if iterate < max_iter else "Done"
    print(pre, "time out based on max_iter limit of", max_iter)

########################################################

########################################################
# Challenge 2 Unzip Zip-Files
########################################################

def decode_QR_Code(img):
    try:
        qr_result = decode(img)
        print(qr_result)

    except Exception:
        print("Img konnte nicht geöffnet werden")

########################################################

########################################################
# Challenge 3 Unzip Zip-Files
########################################################
# Controll every cyber_binary Byte for Byte
def check_Byte(txt):
    count = 0
    for _ in txt:
        count += 1
        if count == 8:
            return txt
    while count < 8:
        txt += str(0)
        count += 1
    return txt


# Function Binary to Ascii-char output
def to_ascii(char):
    return chr(int(char, 2))


# Translate one Byte-block of binaries
def translate(txt):
    result_tmp: str = ''
    letters = txt.split(' ')
    for letter in letters:
        if letter not in '/"':
            byte_var = check_Byte(letter)
            result_tmp += to_ascii(byte_var)
    return result_tmp


def Cyber_Chiffre(file_name):
    string = file_name.read().splitlines()
    NewText = list()
    cyber_binary = ''
    count_index = 0
    num_block = 0  # 1 Byte-Block counter

    # Split lines in Text
    for lines in string:
        if lines.__len__() > 0:
            NewText.append(lines.split())

    # Jedes Wort aus Text einzeln lesen
    for line in NewText:
        for i in line:
            if count_index <= 8:
                if i.__contains__("Cyber-") or i.__contains__("cyber-"):
                    cyber_binary += str(1)
                    count_index = count_index + 1
                elif i.__contains__("Cyber") or i.__contains__("cyber"):
                    cyber_binary += str(0)
                    count_index = count_index + 1

                if cyber_binary.__len__() > 0 and count_index == 8:
                    num_block += 1
                    if num_block < 22:
                        cyber_binary += str(' ')
                    count_index = 0

    return cyber_binary

########################################################
# Challenge 4 Password_Crack
########################################################

def crack(in_filename, wordlist):
   n = len(list(open(wordlist, "rb")))
   zip_file = zipfile.ZipFile(in_filename)
   with open(wordlist, "rb") as file:
      for passwords in tqdm(file, total = n, unit = "passwords"):
         try:
            zip_file.extractall(pwd = passwords.strip())
         except:
            continue
         else:
            print("\nPasswort: ", passwords.decode())
            return passwords.decode()

def unzip(in_filename, password):
    with zipfile.ZipFile(in_filename, 'r') as zip:
        for i in zip.NameToInfo:
            #inside = zip.namelist()[i]
            zip.extract(i,pwd=bytes(password,'utf-8'))



########################################################


########################################################
# Main
########################################################

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Variables
    LEVELS = 2022 # Define max Iteration level
    path='C:/Users/Adrian Höppener/PycharmProjects/CompleteHackDecember2021_v.1/'
    filename='challenge.zip'
    img_a = 'A.png'
    img_b = 'B.png'
    hash_tag=''

    ### PW-Help
    qr_pw = "4ll_i_want_for_X-MAS_is_HACKING!" # Couldnt decode the Content with a script manuelly
    ###
    for _ in range(30):
        hash_tag+='#'

    print(hash_tag)
    print("Start with Challenge #1")
    print(hash_tag)

    try:
        # with zipfile.ZipFile(location) as target:

        unzip_directory_recursively(path,LEVELS)
        print('Unzip file done!')
    except:
        print("Datei konnte nicht gefunden werden!")

    print(hash_tag)
    print('Start with Challenge #2')
    print(hash_tag)

    try:
        im1 = Image.open(img_a).convert(('1'))
        im2 = Image.open(img_b).convert(('1'))

        result = ImageChops.logical_xor(im1, im2)
        result.save(path + 'out.png')
        print("Show Result: ")
        result.show()
    except:
        print("Bilder können nicht miteinander komprimiert werden")
        # See PyCharm help at https://www.jetbrains.com/help/pycharm/


    print(hash_tag)
    print("Decodiere das neu erstellte Bild:")
    print(hash_tag)
    try:

        im3 = Image.open(path + 'out.png')
        print(decode_QR_Code(im3))

        print('Decoding QR-Image done!')
    except:
        print("Fehler mit dem neuen Bild")

    print('Unzip Zipfile')
    filename='next_level.zip'

    try:
        unzip(filename,qr_pw)
    except:
        print("Can't extract Zipfile... Wrong Password!!!")

    print(hash_tag)
    print("Start with Challenge #3")
    print(hash_tag)

    filename = open('cybergedicht.txt', 'r')
    pw_actual = translate(Cyber_Chiffre(filename))
    print("Das Lösungswort aus dem Märchen lautet: " + pw_actual)

    print("Extract fast_geschafft.zip with new received Password")
    filename='fast_geschafft.zip'

    try:
        unzip(filename,pw_actual)
    except:
        print("Can't extract fast_geschafft Zipfile... Wrong Password!!!")

    print(hash_tag)
    print("Start with Challenge #4")
    print(hash_tag)

    filename='flagge.zip'
    print("*********** Crack the Flag now!!!!! ***********")

    solution_word=crack(filename,'rockyou.txt')

    print(hash_tag)
    print("#Solution")
    print(hash_tag)

    print("Das Lösungswort der Challenge lautet:" + solution_word)

    print("Merry Christmas and Happy Hacking New Year 2022 :-)")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
