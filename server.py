import os
import sys

def smtp_response():
    """
    Main function call to generate server responses to SMTP messages in the /forward subdirectory
    """
    forward_files = os.listdir('forward')

    forward_files.extend(os.listdir())

    files_not_to_parse = ['SMTP1.py', 'SMTP2.py', 'tests', 'forward']

    for file in forward_files[:]:
        if file in files_not_to_parse:
            forward_files.remove(file)

    if not forward_files:
        exit('QUIT')

    for file in forward_files:
        msg_arr = read_from_file(file)
        #print("Parsing ", file)
        msg_arr = process_msg(msg_arr)
        #print(msg_arr)

        for line in msg_arr:

            print(line)
            server_response = sys.stdin.readline()
            sys.stderr.write(server_response)
            
            cmd_type = determine_cmd(line)
            
            sys.stderr.write(server_response)
            sys.stderr.flush()

            if cmd_type in [FROM_CMD, TO_CMD] or line[-1] == '.':
                if parse_server_response(server_response) != '250':
                    exit('QUIT')

            elif cmd_type == DATA_CMD:
                if parse_server_response(server_response) != '354':
                    exit('QUIT')


                

def read_from_file(filename):
    """
    Reads valid SMTP messages from /forward and returns an array containing each line of the msg
    """
    msg_arr = []

    with open('forward/'+filename, 'r') as file:
        msg_arr = file.read().splitlines()

    return msg_arr


FROM_CMD = 0
TO_CMD = 1
DATA_CMD = 2


def process_msg(msg_array):
    """
    Changes the format of the message back into it's client-side SMTP format
    """
    updated_msg_array = []
    data_content = []

    for line in msg_array:
        cmd_type = determine_cmd(line)
        
        # If the array body_content is not empty
        if cmd_type == FROM_CMD or cmd_type == TO_CMD:
            
            if data_content:
                updated_msg_array.append("DATA")
                data_content.append('.')
                updated_msg_array.append('\n'.join(data_content))

            cmd_prefix = 'MAIL FROM: ' if cmd_type == FROM_CMD else 'RCPT TO: ' 
            updated_msg_array.append(cmd_prefix + get_address(line))

        elif cmd_type ==  DATA_CMD:
            data_content.append(line)

    if data_content:
        updated_msg_array.append("DATA")
        data_content.append('.')
        updated_msg_array.append('\n'.join(data_content))

    return updated_msg_array


def determine_cmd(line):
    """
    Takes a line from a forward message and determines what part of the message is being parsed

    Returns type
    """
    if line[0:5] == 'From:' or line[0:10] == 'MAIL FROM:':
        return FROM_CMD

    elif line[0:3] == 'To:' or line[0:8] == 'RCPT TO:':
        return TO_CMD

    else:
        return DATA_CMD


def get_address(line):
    address = line.split('<')[1].split('>')[0]
    return f"<{address}>"


def parse_server_response(line):
    """
    Validates an SMTP server response line and extracts the status code.
    Checks for a recognized 3-digit code followed by mandatory whitespace.
    
    Returns:
        3-digit code as a string if valid, 
        -1 otherwise
    """
    if len(line) <= 3:
        return '-1'

    response_num = line[0:3]
    
    valid_cmd = response_num in ['250', '354', '500', '501', '503'] and valid_whitespace(line, 3)
    
    if not valid_cmd:
        return '-1'
    
    return response_num


def valid_whitespace(line, index):
    """
    Checks if the char at the index is a space or tab
    """
    return line[index] == ' ' or line[index] == '\t'

smtp_response()