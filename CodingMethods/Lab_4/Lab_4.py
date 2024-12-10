from twofish import Twofish

T = Twofish(b'00000000')
x = T.encrypt(b'1234567890123456')
print(x)
print(T.decrypt(x).decode())
