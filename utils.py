def remove_accents(text):
    """
    Remove Vietnamese accents from text for better search matching.
    """
    accents = {
        'àáảãạăằắẳẵặâầấẩẫậ': 'a',
        'ÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬ': 'A',
        'èéẻẽẹêềếểễệ': 'e',
        'ÈÉẺẼẸÊỀẾỂỄỆ': 'E',
        'ìíỉĩị': 'i',
        'ÌÍỈĨỊ': 'I',
        'òóỏõọôồốổỗộơờớởỡợ': 'o',
        'ÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢ': 'O',
        'ùúủũụưừứửữự': 'u',
        'ÙÚỦŨỤƯỪỨỬỮỰ': 'U',
        'ỳýỷỹỵ': 'y',
        'ỲÝỶỸỴ': 'Y',
        'đ': 'd',
        'Đ': 'D'
    }
    for accented, plain in accents.items():
        for char in accented:
            text = text.replace(char, plain)
    return text