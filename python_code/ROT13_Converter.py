import codecs

class ROT13_Converter:
    #def __init__(self):
        
    def ROT13_convert(self, str_to_convert, convert_type):
        self.str_to_convert = str_to_convert
        self.convert_type = convert_type
        if self.convert_type == 1:
            str = codecs.encode(self.str_to_convert, 'rot_13')
            return str
        elif self.convert_type == 2:
            str = codecs.decode(self.str_to_convert, 'rot_13')
            return str

def main():
    cls = ROT13_Converter()
    str = cls.ROT13_convert("Lincoln", 1)
    print("String to Convert: " + cls.str_to_convert)
    print("Converted String: " + str)
    
    cls.convert_type = 2
    cls.str_to_convert = str
    str02 = cls.ROT13_convert(str,2)
    print("Convert Back: " + str02)

if __name__ == '__main__':
    main()