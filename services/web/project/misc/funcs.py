
import random
import string

def rand_string(length = 30):
    rand_str = ''.join(random.choice(
                    string.ascii_letters + string.digits) for _ in range(length))
    return(rand_str)

def rand_user_id():
    return("u_"+str(random.randint(1, 1e10)))