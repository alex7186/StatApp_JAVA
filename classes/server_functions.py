from classes.stat_classes import StatAnalysis_2_arr, StatAnalysis_1_arr
from classes.side_functions import _decode_buff_to_bytes
from classes.graph import _1_arr_make_boxplot, _1_arr_make_hist, _1_true_plot
from classes.graph import  _2_arr_reg_plot, _2_arr_make_boxplot

def make_server_diagrams(dict_like_data):

    if dict_like_data['req_type'] == '1_arr':
        return arr_1_server_answer(dict_like_data)

    elif dict_like_data['req_type'] == '2_arr':
        return arr_2_server_answer(dict_like_data)

    else:
        return []

def arr_1_server_answer(data_dict_like):
    arr = data_dict_like['arr_data']

    sr_methodics = data_dict_like['sr_met']
    true_value = data_dict_like['true_value']
    make_text = data_dict_like['make_text']
    make_hist = data_dict_like['make_hist']
    make_boxplot = data_dict_like['make_boxplot']

    result = [
        {'type':'text',  'show_index':0, 'content': ""},
        {'type':'image', 'show_index':1, 'content': ""},
        {'type':'text',  'show_index':2, 'content': ""},
        {'type':'image', 'show_index':3, 'content': ""},
        {'type':'text',  'show_index':4, 'content': ""},
        {'type':'image', 'show_index':5, 'content': ""},
    ]

    if make_text or (true_value > -1):
        analysis = StatAnalysis_1_arr(
            arr, 
            sr_methodics=sr_methodics, 
            true_value=true_value)
        text_arr = analysis.res_text[0]
        result[0]['content'] = text_arr[0]

    if make_hist:
       result[1]['content'] = _decode_buff_to_bytes(
        _1_arr_make_hist(sorted(arr)))
    
    if make_text:
        result[2]['content'] = text_arr[1]
    
    if make_boxplot:
       result[3]['content'] = _decode_buff_to_bytes(
        _1_arr_make_boxplot(sorted(arr)))
    
    if make_text:
        result[4]['content'] = text_arr[2]

    if true_value > -1:
       result[5]['content'] = _decode_buff_to_bytes(
        _1_true_plot(arr, true_value))

    return result

def arr_2_server_answer(data_dict_like):
    arr1 = data_dict_like['arr1']
    arr2 = data_dict_like['arr2'] 
    make_text = data_dict_like['make_text']
    make_boxplot = data_dict_like['make_boxplot']

    result = [
        {'type':'text',  'show_index':0, 'content': ""},
        {'type':'image', 'show_index':1, 'content': ""},
        {'type':'image', 'show_index':2, 'content': ""},
        {'type':'text',  'show_index':3, 'content': ""},
        # {'type':'image', 'show_index':2, 'content': ""},
    ]

    if make_text:
        text_arr = StatAnalysis_2_arr(arr1, arr2).res_text[0]
        result[0]['content'] = text_arr[0]
    if len(arr1) == len(arr2):
        result[1]['content'] = _decode_buff_to_bytes(
            _2_arr_reg_plot(arr1, arr2))
    if make_boxplot:
        result[2]['content'] = _decode_buff_to_bytes(
            _2_arr_make_boxplot(sorted(arr1), sorted(arr2)))
    if make_text:
        result[3]['content'] = text_arr[1]

    return result