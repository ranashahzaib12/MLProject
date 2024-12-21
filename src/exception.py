import sys

# Custoom Exception handling Library 
def error_message_detail(error, error_detail: sys):
    """
    This function generates a detailed error message, including the file name, 
    line number, and error message from the exception.
    """
    _, _, exc_tb = error_detail.exc_info()  # Extract execution info
    file_name = exc_tb.tb_frame.f_code.co_filename  # Get the file name
    line_number = exc_tb.tb_lineno  # Get the line number
    error_message = "Error occurred in Python script: [{0}] at line number [{1}] with error message [{2}]".format(
        file_name, line_number, str(error)
    )
    return error_message

class CustomException(Exception):
    def __init__(self,error_message ,error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message ,error_detail= error_detail)

    def __str__(self):
        return self.error_message 