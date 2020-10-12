
import random
import string

def rand_string(length):
    rand_str = ''.join(random.choice(
                    string.ascii_letters + string.digits) for _ in range(length))
    return(rand_str)