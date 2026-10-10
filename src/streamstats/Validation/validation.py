# class Validate
#
# class ValidateCsv:
#     def check_valid_stroke(cls, header, cell):
#         if header == cls.OBLIGATORY_HEADERS[0]:
#             valid_strs = cell.split(" ")
#             valid = True
#             if valid_strs[0] != "ISO":
#                 valid = False
#             for char in valid_strs[1]:
#                 if char not in cls.nums:
#                     valid = False
#                     break
#             if not valid:
#                 raise WrongObligatoryCellError("One of your cells in 'timestamp' has wrong format!")
