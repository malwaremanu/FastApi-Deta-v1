import base64, json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad

#AES ECB mode without IV

data = str({
    "data" : "i love coomputer science"
})

key = 'AAAAAAAAAAAAAAAA' #Must Be 16 char for AES128

def encrypt(raw):
        raw = pad(raw.encode(),16)
        cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
        return base64.b64encode(cipher.encrypt(raw)).decode("utf-8", "ignore")

def decrypt(enc):
        enc = base64.b64decode(enc)
        cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
        return json.loads(unpad(cipher.decrypt(enc),16).decode("utf-8", "ignore"))

print(decrypt("oXeW41FAA4kdTU63rIwVdlvGvqqiquF22gm+15jXi4W/NZhWdESADG/ZYrIeMj/Y"))