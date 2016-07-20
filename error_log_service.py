import traceback
import csv
from datetime import date, datetime
import os.path

# Global configs
ERROR_LOG = 'errors.csv'

class ErrorLogService:
    err_fields = ['Date', 'Time', 'Severity', 'Message', 'Exception']

    def __create_error_log_row(self, message, severity, exception):
        """ Creates an error formatted for a row in a csv document """
        try:
            row = {self.err_fields[0]: date.today().strftime("%d/%m/%Y"),
                    self.err_fields[1]: datetime.now().time().strftime("%I:%M %p %Z"),
                    self.err_fields[2]: severity,
                    self.err_fields[3]: message,
                    self.err_fields[4]: exception }
        except:
            print("ERROR: failed to create error field rows")
            print(traceback.format_exc())
            row = None
        return row

    def log_error(self, message, severity, exception=""):
        """ Writes an error to a csv file as a single row """
        error_row = self.__create_error_log_row(message, severity, exception)
        if not error_row:
            print("ERROR: a problem occurred, error logging is unable to continue")
            print(traceback.format_exc())
            return

        try:
            is_new_file = not os.path.isfile(ERROR_LOG)
            with open(ERROR_LOG, 'a+') as err_log_file:
                writer = csv.DictWriter(err_log_file, delimiter=',', dialect='excel', 
                                        fieldnames=self.err_fields) 
                if is_new_file:
                    writer.writeheader()
                writer.writerow(error_row)
        except:
            print("WARNING: Unable to open error log file. No errors will be logged. Is the error log file open?")
            print(traceback.format_exc())
            
        if severity.lower() == "fatal":
            raise CustomException(message)

class CustomException(Exception):
    def __init__(self, value):
        self.value = value