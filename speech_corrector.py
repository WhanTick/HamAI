import re

# Expanded dictionary of Indonesian slang and their full forms
slang_dict = {
    "knp": "kenapa",
    "gmn": "gimana",
    "bg": "bang",
    "cok": "co",
    "emg": "emang",
    "gw": "gua",
    "gblk": "goblok",
    "lu": "lo",
    "yg": "yang",
    "tp": "tapi",
    "udh": "udah",
    "blm": "belum",
    "td": "tadi",
    "sm": "sama",
    "aja": "saja",
    "bgt": "banget",
    "dgn": "dengan",
    "dlu": "dulu",
    "krn": "karena",
    "bsk": "besok",
    "tdk": "tidak",
    "sy": "saya",
    "tmn": "teman",
    "jg": "juga",
    "ajg": "anjing",
    "yaudh": "ya udah",
    "bru": "baru",
    "bgst": "bangsat",
    "syg": "sayang",
    "kyk": "kayak",
    "ngmng": "ngomong",
    "ngapa2in": "ngapa-ngapain",
    "y": "iya",
    "kgk": "kaga",
    "msh": "masih",
    "jan": "jangan",
    "bkin": "bikin",
    "bgs": "bagus",
    "pgn": "pengen",
    "lg": "lagi",
    "skrg": "sekarang",
    "smua": "semua",
}

def expand_slang(text):
    # Split text while preserving punctuation
    words = re.findall(r'\b\w+\b|\S', text)
    # Replace slang words
    expanded_words = [slang_dict.get(word.lower(), word) for word in words]
    return ' '.join(expanded_words)
