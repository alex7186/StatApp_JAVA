from base64 import b64encode
# from base64 import b64decode

def _decode_buff_to_bytes(input_buff):
    input_base64 = b64encode(input_buff.getvalue())

    return input_base64.decode('ascii')


# def _encode_bytes_to_buff(input_str):
#     return b64decode(input_str)

def custom_round(number, deg):
    try:
        number_str = format(float(number), '.10f').split('.')
        num1 = number_str[0]
        num2 = number_str[1]
    except Exception:
        raise ValueError('String.valueof() ERROR')

    res = '0.0'

    if False:
        pass

    elif deg == len(num1):
        res = float(num1) + int(round(float('0.' + str(num2)), 0))
        res = str(res)

    elif deg > len(num1) + len(num2):
        res = num1 + '.' + num2 + '0' * (deg - (len(num1) + len(num2)))

    elif deg < len(num1) + len(num2):
        if len(num1) < deg:
            res = num1 + '.' + num2
            
            res = round(float(res), deg - len(num1))
            res_str = format(res, '.10f')

            num1 = res_str.split('.')[0]
            num2 = res_str.split('.')[1]
            res = str(res) + '0' * (deg - len(num1) - len(num2))

    elif deg == len(num1) + len(num2):
        res = num1 + '.' + num2

    elif deg == len(num1):
        res = 1 if round(float('.' + num2), 0) == 1.0 else 0
        res = float(num1) + res

    elif deg < len(num2):  # 0.0004 3
        res = round(num2, deg - 1)
        res = num1 + '.' + res

    return repair_mantice(res, deg)


def repair_mantice(res, deg: int):
    if '.' in str(res):
        return (str(res) + "00000000000000")[:deg + 1]
    else:
        return (str(res) + "00000000000000")[:deg]


def get_meaning_count(number):
    s = str(number).replace('.', '').replace('-', '')
    return int(len(s))

def define_distribution_type(arr, make_formula=True, make_title=True):
        return None

F_table = {
    3:{
        3: 9.28,4: 6.59,5: 5.41,6: 4.76,7: 4.35,8: 4.07,9: 3.86,10: 3.71,
        11: 3.59,12: 3.49,13: 3.41,14: 3.34,15: 3.29,16: 3.24,17: 3.20,18: 3.16,
        19: 3.13,20: 3.10,
    },
    4:{
        3: 9.12,4: 6.39,5: 5.19,6: 4.53,7: 4.12,8: 3.84,9: 3.63,10: 3.48,
        11: 3.36,12: 3.26,13: 3.18,14: 3.11,15: 3.06,16: 3.01,17: 2.96,18: 2.93,
        19: 2.90,20: 2.87,
    },
    5:{
        3: 9.01,4: 6.26,5: 5.05,6: 4.39,7: 3.97,8: 3.69,9: 3.48,10: 3.33,
        11: 3.20,12: 3.11,13: 3.03,14: 2.96,15: 2.90,16: 2.85,17: 2.81,18: 2.77,
        19: 2.74,20: 2.71,
    },
    6:{
        3: 8.94,4: 6.16,5: 4.95,6: 4.28,7: 3.87,8: 3.58,9: 3.37,10: 3.22,
        11: 3.09,12: 3.00,13: 2.92,14: 2.85,15: 2.79,16: 2.74,17: 2.70,18: 2.66,
        19: 2.63,20: 2.60,
    },
    7:{
        3: 8.89,4: 6.09,5: 4.88,6: 4.21,7: 3.79,8: 3.50,9: 3.29,10: 3.14,
        11: 3.01,12: 2.91,13: 2.83,14: 2.76,15: 2.71,16: 2.66,17: 2.61,18: 2.58,
        19: 2.54,20: 2.51,
    },
    8:{
        3: 8.85,4: 6.04,5: 4.82,6: 4.15,7: 3.73,8: 3.44,9: 3.23,10: 3.07,
        11: 2.95,12: 2.85,13: 2.77,14: 2.70,15: 2.64,16: 2.59,17: 2.55,18: 2.51,
        19: 2.48,20: 2.45,
    },
    9:{
        3: 8.81,4: 6.00,5: 4.77,6: 4.10,7: 3.68,8: 3.39,9: 3.18,10: 3.02,
        11: 2.90,12: 2.80,13: 2.71,14: 2.65,15: 2.59,16: 2.54,17: 2.49,18: 2.46,
        19: 2.42,20: 2.39,
    },
    10:{
        3: 8.79,4: 5.96,5: 4.74,6: 4.06,7: 3.64,8: 3.35,9: 3.14,10: 2.98,
        11: 2.85,12: 2.75,13: 2.67,14: 2.60,15: 2.54,16: 2.49,17: 2.45,18: 2.41,
        19: 2.38,20: 2.35,
    },

}

Xi_table = {
    2: 5.994,3: 7.815,4 : 9.488,5 : 11.071,
    7 : 14.067,8 : 15.507,9 : 16.919,10 : 18.307,
    11 : 19.675,12 : 21.026,13 : 22.362,14 : 23.685,
    15 : 24.996,16 : 26.296,17 : 27.587,18 : 28.869,
    19 : 30.144,20 : 31.410,21 : 32.671,22 : 33.924,
    23 : 35.172,24 : 36.415,25 : 37.652,
}

Q_criterion = {
    3: 0.97, 4: 0.829, 5: 0.71,
    6: 0.625, 7: 0.568, 8: 0.526,
    9: 0.493, 10: 0.466, 11: 0.444,
    12: 0.426, 13: 0.410, 14: 0.396,
    15: 0.384, 16: 0.374, 17: 0.365,
    18: 0.356, 19: 0.349, 20: 0.342,
    21: 0.337, 22: 0.331, 23: 0.326,
    24: 0.321, 25: 0.317, 26: 0.312,
    27: 0.308, 28: 0.305, 29: 0.301,
    30: 0.290
}

t_criterion = {
    2: 5.991,
    3: 3.1825,
    4: 2.7764, 5: 2.5706, 6: 2.4469,
    7: 2.3646, 8: 2.3060, 9: 2.2622,
    10: 2.2281, 11: 2.2010, 12: 2.1788,
    13: 2.1604, 14: 2.1448, 15: 2.1315,
    16: 2.1199, 17: 2.1098, 18: 2.1009,
    19: 2.0930, 20: 2.0860, 21: 2.0796,
    22: 2.0739, 23: 2.0687, 24: 2.0639,
    25: 2.0595, 26: 2.0555, 27: 2.0518,
    28: 2.0484, 29: 2.0452, 30: 2.0423,
}