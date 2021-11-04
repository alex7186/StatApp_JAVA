class BaseClass():
    def __init__(self,):

        self.res_text = [[] '']
        self.log_res_text = True

        self.more_symbol = "&gt;" # "->-"
        self.less_symbol = "&lt;" # "-<-"

    def get_array_meaning_count(self, arr):
        return max([get_meaning_count(el) for el in arr])

    def accept_arr(self, arr):
        if len(arr) < 3:
            raise ValueError('The array is too short')
        return arr

    def add_res_text(self, text):
        if self.log_res_text:
            self.res_text[1] += text

    def confirm_res_text(self):
        self.res_text[0].append(self.res_text[1])
        self.res_text[1] = ''

    def custom_round(self, number, deg=None):
        if deg == None:
            return cr(number, self.meaning_count)
        else:
            return cr(number, deg)

    def get_mean(self, arr, label=' '):
        mean = np_mean(arr)
        res = """\n\nСреднее значение {} :\n\tx̅{} = {}""".format(
            label,
            label[-1],
            self.custom_round(mean))
        self.add_res_text(res)
        return mean

    def get_dispersion(self, 
        arr, mean, mean_str, label=' ', make_formula=True, make_title=True):

        S = (
            sum(
                [(el - float(mean)) ** 2 for el in arr]
                ) / (
                len(arr) - 1
                )
            ) ** 0.5

        S_str = self.custom_round(S, self.meaning_count)

        Sr = float(S) / mean
        
        Sr_str = self.custom_round(Sr, self.meaning_count)


        if self.log_res_text:
            res = ("""\n\nСтандартное и относительное стандартное отклонения:""" if make_title else "") + \
                ("""\n\tS = √(Σ(Xi - x̅)^2 / (n-1)) """ if make_formula else '') + \
                 """\n\n\tS{} = √(Σ(Xi - {})^2 / ({}-1)) """.format(label[-1], mean_str, len(arr), ) + \
                """\n\tS{} = {}\n""".format(label[-1], S_str, ) + \
                ("""\n\tSr = S / x̅ """  if make_formula else '') + \
                """\n\tSr{} = {} / {} """.format(label[-1], S_str, mean_str, ) + \
                """\n\tSr{} = {}""".format(label[-1], Sr_str)

            self.add_res_text(res)

        return (S, Sr)