#awesome functions to set or clear the LSB using bit manipulations
def set_last_bit(num):
    return num | 1

def clear_last_bit(num):
    return num & ~1

#convert string to binary
def return_binary(mystring):
    mystring = mystring.encode()
    mystring = int.from_bytes(mystring,'big')
    mystring = bin(mystring)[2:]
    return mystring

#convert binary to string
def return_text(mystring):
    binNum = int('0b' + mystring, 2)
    return binNum.to_bytes((binNum.bit_length() + 7) // 8, 'big').decode()
