import sys
import string

"""
@author: Will Minor


Parser developed to validate SMTP commands

SMTP (Simple Mail Transfer Protocol) is a protocol used for sending messages from a mail server or a mail client (i.e. gmail) to another mail server.

Commands are constrained by the following grammar:

<mail-from-cmd> ::= “MAIL” <whitespace> “FROM:” <nullspace> <reverse-path> <nullspace> <CRLF>
"""


"""
cmd (String): the file or input of SMTP commands to parse and validate

Uncomment (1) to input from a file via command:  'python parse.py < <file_name.txt>'
Uncomment (2) to input from keyboard
"""

"""(1)"""
cmd = sys.stdin.read()
"""(2)"""
#cmd = input("Type an SMTP command\n")


# Array to hold list of  dec values of special ASCII vals
ascii_special_arr = [60, 62, 40, 41, 91, 93, 92, 46, 44, 59, 58, 64, 34]

# Index of the current character being evaluated by the parser
c = 0

# Default status message indicating a parse was completed with no errors
status_message = "Sender ok"

# Bool flag that raises when an error in the parse is detected
error_exists = False


def curr_char():
    """
    Used in conditional statements to check current character

    Returns: 
        current char being evaluated by parser
    """
    if c >= len(cmd):
        return None
    return cmd[c]


def next_char():
    """
    Returns: 
        char that comes after current char
    """
    if c+1 >= len(cmd):
        return None
    return cmd[c+1]


def consume(num):
    """
    Consumes the current char, which incriments index of parser
    To be used in the case that a character is valid

    Args:
        num (int): Amount of characters to consume (typically 1)
    """
    global c
    c+=num


def error_msg(error_msg):
    """
    Sets status message to a specific error message string

    Once it catches one error message, each following error message won't be reported
    """
    global error_exists
    if not error_exists:
        set_status_msg(error_msg)
        error_exists = True

    
def set_status_msg(msg):
    """
    Helper function to set the global status_message

    Args:
        msg (String): Status message to be set
    """
    global status_message
    status_message = msg


def print_status_msg():
    """
    Helper function that prints global status_message
    """
    global status_message
    print(status_message)


def echo_cmd(starting_index):
    """
    Prints the current command being evaluated by the parser

    Args:
        index1 (int): Starting index of the parse (c), should be stored by a temp variable in parse_main()
    """
    global c
    print(cmd[starting_index:c].rstrip('\n'))


def skip_to_crlf():
    """
    In the case that an error is detected before parse_crlf(), this func is called to skip to <crlf>
    """
    global c

    while c < len(cmd) and curr_char() != '\n':
        c+=1

    if c < len(cmd):
        c+=1


def parse_mail_from_cmd():
    """
    Parser that calls recursive descent functions for 'MAIL FROM:' SMTP commands
    """
        
    global error_exists

    start_index = c

    parse_mail()

    parse_whitespace()

    parse_from()

    parse_nullspace()

    parse_reverse_path()

    parse_nullspace()

    """
    If-else block ensures that multiple commands issued in one newline are flagged as <CRLF> error
    """
    if error_exists:
        skip_to_crlf()
    else:
        parse_crlf()
        if error_exists:
            skip_to_crlf()
        error_msg("250 OK")
        
    echo_cmd(start_index)

    print_status_msg()

    error_exists = False
        

def parse_rcpt_to_cmd():
    
    global c, error_exists
    
    while peek_cmd() == RCPT_STATE:
        
        start_index = c

        parse_rcpt()

        parse_whitespace()

        parse_to()

        parse_nullspace()

        parse_reverse_path()

        if error_exists:
            skip_to_crlf()
        else:
            parse_crlf()
            if error_exists:
                skip_to_crlf()
            error_msg("250 OK")
            error_exists = False

        echo_cmd(start_index)
        print_status_msg()


def parse_data_cmd():

    global c, error_exists
    
    start_index = c

    parse_data()

    parse_nullspace()

    if error_exists:
        skip_to_crlf()
        error_exists = False
        print("here")
        error_exists = True
    else:
        parse_crlf()
        if error_exists:
            skip_to_crlf()
            set_status_msg("500 Syntax error: command unrecognized")
        else:
            error_msg("354 Start mail input; end with <CRLF>.<CRLF>")
            error_exists = False
    
    echo_cmd(start_index)

    print_status_msg()


def parse_data_input():
    global c
    
    while True:
        if c >= len(cmd):
            break

        if curr_char() == '.' and (c > 0 and cmd[c-1] == '\n'):
            if (c + 1 < len(cmd)) and cmd[c+1] == '\n':
                print(".")
                consume(2)
                print("250 OK")
                reset_state()
                return
        
        print(curr_char(), end='')
        consume(1)


def parse_main():
    
    global error_exists, current_state

    while c < len(cmd):
        if not valid_state():
            error_exists = False 
            continue

        if current_state == MAIL_STATE:
            parse_mail_from_cmd()
            if error_exists:
                reset_state()
                error_exists = False
                continue
            else:
                transition_state()
        
        elif current_state == RCPT_STATE:
            parse_rcpt_to_cmd()
            if error_exists:
                reset_state()
                error_exists = False
                continue
            elif not error_exists and peek_cmd() == DATA_STATE:
                transition_state()

        elif current_state == DATA_STATE:
            parse_data_cmd()
            if not error_exists:
                parse_data_input()
            reset_state()

        error_exists = False
        

def peek_cmd():
    if valid_mail_cmd():
        return MAIL_STATE

    elif valid_rcpt_cmd():
        return RCPT_STATE
    
    elif valid_data_cmd():
        return DATA_STATE
    
    else:
        return INVALID_STATE


def valid_state():
    global c, current_state
    start_char = c
    peek_state = peek_cmd()
    
    if curr_char() == None:
        return False

    if peek_state == INVALID_STATE:
        error_msg("500 Syntax error: command unrecognized")
        skip_to_crlf()
        echo_cmd(start_char)
        print_status_msg()
        reset_state()
        return False

    elif peek_state != current_state:
        error_msg(f"503 Bad sequence of commands")
        skip_to_crlf()
        echo_cmd(start_char)
        print_status_msg()
        reset_state()
        return False

    else:
        return True


def reset_state():
    global current_state, error_exists
    current_state = MAIL_STATE


def transition_state():
    """
    Cycles to the next state in the state-machine by incrimenting current_state by 1. If state reaches out of bounds, calls reset_state() 
    """
    global current_state
    current_state += 1

    if current_state > DATA_STATE:
        reset_state()


def valid_mail_cmd():
    """
    Checks that the next cmd input is a 'MAIL FROM:' cmd
    """
    global c, error_exists
    temp = c
    temp_error_exists = error_exists
    error_exists = False
    parse_mail()
    parse_whitespace()
    parse_from()
    c = temp
    
    valid = not error_exists
    error_exists = temp_error_exists

    return valid


def valid_rcpt_cmd():
    """
    Checks that the next cmd input is a 'RCPT TO:' cmd
    """
    global c, error_exists
    temp = c
    temp_error_exists = error_exists
    error_exists = False
    parse_rcpt()
    parse_whitespace()
    parse_to()
    c = temp

    valid = not error_exists
    error_exists = temp_error_exists
    return valid


def valid_data_cmd():
    global c, error_exists
    
    temp = c
    temp_error_exists = error_exists
    error_exists = False
    parse_data()
    c = temp

    valid = not error_exists
    error_exists = temp_error_exists
    return valid


MAIL_STATE = 0
RCPT_STATE = 1
DATA_STATE = 2
INVALID_STATE = -1

STATES = [MAIL_STATE, RCPT_STATE, DATA_STATE]
current_state = 0


def valid_mail():
    """
    Validates that the first 4 characters of MAIL FROM cmd are 'MAIL'
    Returns:
        bool: True if first 4 chars are 'MAIL'
    """
    global c
    return cmd[c:c+4] == "MAIL"


def parse_mail():
    """
    Ensures first 4 chars of MAIL FROM cmd are 'MAIL' and consumes

    Errors:
        If start of cmd is missing 'MAIL' 
    """
    if not valid_mail():
        error_msg("500 Syntax error: command unrecognized")
    consume(4)


def parse_rcpt():
    """
    Ensures first 4 chars of an RCPT cmd is the string 'RCPT' and consumes

    Errors:
        If start of cmd is missing 'RCPT' 
    """
    global c
    if not cmd[c:c+4] == "RCPT":
        error_msg("500 Syntax error: command unrecognized")
    consume(4)


def parse_data():
	"""
    Ensures first 4 chars of a data cmd is the string 'DATA' and consumes

    Errors:
        If start of cmd is missing 'DATA' 
    """
	global c
	if not cmd[c:c+4] == "DATA":
		error_msg("500 Syntax error: command unrecognized")
	consume(4)


def valid_sp(): 
    """
    Checks if current char is a tab or a space

    If so, consumes char

    Returns:
        bool: True if current char is valid space, 
              False otherwise
    """
    return curr_char() == ' ' or curr_char() == '\t'


def parse_sp():
    """
    Consumes current char if it is a tab or a space

    Returns:
        bool: True if current char is valid space, 
              False otherwise
    """
    if valid_sp():
        consume(1)
        return True

    return False


def parse_whitespace():
    """
    Calls parse_sp() to check if current character is valid <whitespace>
    Consumes than recursively calls until no more <whitespace> to consume

    Errors:
        If current character is not a tab or space
    """
    if curr_char() == None:
        error_msg("ERROR -- whitespace")
        return

    if not parse_sp():
        error_msg("500 Syntax error: command unrecognized")

    while valid_sp():
        parse_sp()


def parse_from(): 
    """
    Ensures next 5 chars after <whitespace> in <mail-from-cmd> are 'FROM:' and consumes

    Errors:
        If  cmd is missing 'FROM' 
    """
    global c
    if not cmd[c:c+5] == "FROM:":
        error_msg("500 Syntax error: command unrecognized")
    consume(5)


def parse_to():
    """
    Ensures next 3 chars after <whitespace> in <rcpt-to-cmd> are 'TO:' and consumes

    Errors:
        If cmd is missing 'TO:'
    """
    global c
    if not cmd[c:c+3] == "TO:":
        error_msg("500 Syntax error: command unrecognized")
    consume(3)


def parse_crlf():
    """
    Parses <CRLF> indicating the end of an SMTP command line, if valid consumes it

    Errors:
        If the command line does not terminate with CRLF
    """
    if curr_char() != '\n':
        error_msg("501 Syntax error in parameters or arguments")
    else:
        consume(1)


def parse_nullspace():
    """
    Essentially the same as parse_whitespace(), but allows null inputs
    
    If curr_char() is a <whitespace> calls parse_whitespace() to recursively consume it
    """
    while curr_char() == ' ' or curr_char() == '\t':
        parse_whitespace()


def valid_letter(character):
    """
    Validates if a char is a lowercase (a-z) or uppercase (A-Z) letter

    Assigns ascii_val to the ASCII decimal of curr char, and checks if in range of a valid letter

    Returns:
        bool: True if character is a letter
              False if not
    """
    ascii_val = ord(character)

    return ascii_val in range(65,91) or ascii_val in range(97,123)


def parse_letter():
    """
    Parses <letter> then consumes it

    Returns:
        bool: True if curr char is a letter
              False if not
    """
    if valid_letter(curr_char()):
        consume(1)
        return True

    return False


def parse_digit():
    """
    Checks if curr char is a <digit>

    Assigns ascii_val to the ASCII decimal of curr char, and checks if in range of decimals (0-9)

    If so, consumes char

    Returns:
        bool: True if curr char is a <digit>
              False if not
    """
    ascii_val = ord(curr_char())

    if ascii_val in range(48,58):
        consume(1)
        return True

    return False


def valid_char():
    """
    Checks if curr char is a valid <char> (as defined by grammar)

    Assigns ascii_val to the ASCII decimal of curr char, and checks if in range of valid char inputs for strings

    Checks if ascii_val is of the array of disallowed special chars

    Returns:
        bool: True if curr char is a valid <char>
              False if not
    """
    ascii_val = ord(curr_char())
    
    if ascii_val not in range(33, 127):
        return False

    if ascii_val in ascii_special_arr:
        return False

    return True


def parse_char():
    """
    Cheks if char is and consumes it

    Returns:
        bool: True if char is valid
              False if not
    """
    if valid_char():
        consume(1)
        return True

    return False


def parse_string():
    """
    Recursively parses a <string> that is composed of <char>

    Must have at least one valid <char>

    Returns
        bool: True if atleast one valid char
              False if not
    """
    if not parse_char():
        return False

    if valid_char():
        return parse_string()

    return True


def parse_local_part():
    """
    Parses <local-part> of <mailbox> grammar

    Ensures there's atleast one <char> in <local-part>

    Returns:
        bool: Trace of parse_string()
    """
    return parse_string()


def parse_let_dig():
    """
    Parses <let-dig>, allows char to be a <letter> or a <digit>

    Returns:
        bool: True if char is <let-dig>
              False if not
    """
    return parse_letter() or parse_digit()


def parse_let_dig_str():
    """
    Recursively parses a string of <let-dig>, requiring at least one <let-dig> char

    Returns:
        bool: True if atleast one <let-dig>
              False if not
    """
    if not parse_let_dig():
        return False

    if parse_let_dig():
        parse_let_dig_str()
    else:
        return True


def parse_name():
    """
    Recursively parses <name> which requires at least one <letter> and at least one <let-dig-str>

    Returns:
        bool: True if both above conditions are valid
              False if not
    """
    return parse_letter() and parse_let_dig_str()


def parse_element():
    """
    Parses <element> which can be composed of one <letter> or a <name>

    Returns:
        bool: True if one of above conditions are valid
              False if not
    """
    global c
    if parse_letter():
        c-=1
        parse_name()
        return True
    
    return False

def parse_domain():
    """
    Parses <domain> which can be composed of one element or consecutive elements with '.' between them

    Calls <parse_element> to ensure one valid element, then recusrively calls itself if '.' is detected

    Returns:
        bool:
            True is elements are arranged correctly
            False if not
    """
    if not parse_element():
        return False
    
    if curr_char() == '.':
        consume(1)
        return parse_domain()

    return True


def parse_mailbox():
    """
    Parses <mailbox> in the form: <local-part> + '@' + <domain>

    Calls <parse_local_part> to validate the local-part, checks for the '@'
    separator, then calls <parse_domain> to validate the domain portion.

    Errors:
        If <local-part> is invalid
        If '@' separator is missing
        If <domain> is invalid
    """ 
    if not parse_local_part():
        error_msg("501 Syntax error in parameters or arguments")
    
    if curr_char() == '@':
        consume(1)
    else: 
        error_msg("501 Syntax error in parameters or arguments")
    
    if not parse_domain():
        error_msg("501 Syntax error in parameters or arguments")


def parse_path():
    """
    Parses <path> in the form: '<' +  <mailbox> + '>'

    Ensures the path begins with '<', calls <parse_mailbox> to validate the
    enclosed mailbox, and ensures the path ends with '>'.

    Errors:
        If opening '<' is missing
        If <mailbox> is malformed
        If closing '>' is missing
    """
    if curr_char() != '<':
        error_msg("501 Syntax error in parameters or arguments")
    else:
        consume(1)
    
    parse_mailbox()

    if curr_char() != '>':
        error_msg("501 Syntax error in parameters or arguments")
    else:
        consume(1)


def parse_reverse_path():
    parse_path()


try:
    parse_main()
except IndexError:
    print("ERROR -- msg index")