### Numa situaçao real esta funçao nao estaria a ser chamda desta forma
from cryptography.fernet import Fernet

def info():
    with open('filekey.key', 'rb') as filekey:
        key = filekey.read()
    fernet = Fernet(key)

    # opening the encrypted file
    with open('file', 'rb') as enc_file:
        encrypted = enc_file.read()

    # decrypting the file
    decrypted = fernet.decrypt(encrypted)

    # opening the file in write mode and
    # writing the decrypted data
    with open('file', 'wb') as dec_file:
        dec_file.write(decrypted)
    f = open("file", "r")
    arr=f.readlines()
    print(arr)
    for i in range(len(arr)):
        arr[i]=arr[i].replace("\n","")
        arr[i]=arr[i].replace("#","")
        arr[i]=arr[i].replace("@","a")
        arr[i]=arr[i][::-1]
    print(arr)
    with open('file', 'wb') as encrypted_file:
        encrypted_file.write(encrypted)
