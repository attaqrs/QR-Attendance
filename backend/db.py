import json

database = {}

def start_session(hash):
    database[hash] = set()
    print(f'[INFO]: [{hash}] Started new session')

def mark_attendance(hash, prn):
    if hash not in database:
        error = f'[ERROR]: [{hash}] Invalid hash.'
        print(error)
        return error
    database[hash].add(prn)
    info = f'[INFO]: [{hash}] {prn}\'s request has been processed.'
    print(info)
    return info

def end_session(hash):
    if hash not in database:
        error = f'[ERROR]: [{hash}] Invalid hash.'
        print(error)
        return error
    with open(f'logs/{hash}.json', 'w') as f:
        present_prns = list(database[hash])
        json.dump(present_prns, f)
    del database[hash]
    print(f'[INFO]: [{hash}] Ended session')
    return present_prns

