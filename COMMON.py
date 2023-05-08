import datetime


def print_execution_time(stared):

    finished = datetime.datetime.now()
    print('STARTED TIME  : ' + stared.strftime("%H:%M:%S %d/%m/%Y"))
    print('FINISHED TIME : ' + finished.strftime("%H:%M:%S %d/%m/%Y"))
    print('EXECUTION TINE: ' + str(finished - stared))
