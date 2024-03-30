import csv

validation_flag: bool = False


def float_validation(input: str) -> float:
    if input == '':
        validation_flag = True
        return 0.0
    else:
        return float(input)    


with open ('statcast_data_calls_all.csv','r') as csv_file:
    csv_reader = csv.reader(csv_file)

    with open('new_statcast_data_calls_all.csv', 'w') as new_file:
        csv_writer = csv.writer(new_file, delimiter=',', lineterminator='\n')

        headers: list = next(csv_reader)
        headers.append("correct_call")
        csv_writer.writerow(headers)

        for line in csv_reader:
            validation_flag = False
            call_type: str = line[21]
            plate_x: float = float_validation(line[29])
            plate_z: float = float_validation(line[30])
            sz_top: float = float_validation(line[50])
            sz_bot: float = float_validation(line[51])
            sz_hor: float = 0.83
            baseball_rad : float = 0.120833
            correct_call: int = 1
            
            if validation_flag:
                continue
            elif (abs(plate_x) > sz_hor) and (call_type == 'S'):
                correct_call = 0
            elif (abs(plate_x) < sz_hor) and (plate_x < (sz_top + baseball_rad)) and (plate_x > (sz_bot - baseball_rad)) and (call_type == 'B'):
                correct_call = 0
            elif (plate_z < (sz_top + baseball_rad)) and (plate_z > (sz_bot - baseball_rad)) and (abs(plate_x) < sz_hor) and (call_type == 'B'):
                correct_call = 0
            elif (plate_z > (sz_top + baseball_rad)) and (call_type == 'S'):
                correct_call = 0
            elif (plate_z < (sz_bot - baseball_rad)) and (call_type == 'S'):
                correct_call = 0
                
            line.append(correct_call)
            csv_writer.writerow(line)