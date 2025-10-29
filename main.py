import argparse
from pykeepass import PyKeePass
from multiprocessing import Pool
import time
import os
from tqdm import tqdm

def try_password(args):
    index, password, database_path, keyfile_path = args
    password = password.strip()
    try:
        PyKeePass(database_path, password=password, keyfile=keyfile_path)
        return password
    except Exception: # CredentialsError
        return None

def main():
    parser = argparse.ArgumentParser(
        description="simple multi-process brute-force tool for KeePass (.kdbx) files. Works with password-only or password+keyfile setups."
    )
    parser.add_argument("-d", "--database", type=ascii, required=True, help="Path to the KeePass .kdbx file")
    parser.add_argument("-w", "--wordlist", type=ascii, required=True, help="Text file with passwords to try, one per line")
    parser.add_argument("-k", "--keyfile", type=ascii, required=False, help="Optional keyfile to use if the database requires it")
    parser.add_argument("-t", "--threads", type=int, default=os.cpu_count(), help="Number of parallel processes to use (default: all CPU cores)")
    args = parser.parse_args()

    db_file = args.database.replace("'", "")
    wordlist_file = args.wordlist.replace("'", "")
    keyfile_path = args.keyfile.replace("'", "") if args.keyfile else None
    num_threads = args.threads

    print(f"Database file : {db_file}")
    print(f"Wordlist      : {wordlist_file}")
    if keyfile_path:
        print(f"Keyfile       : {keyfile_path}")


    max_threads = os.cpu_count()
    if num_threads < 1:
        print("Thread count too low. Using 1 thread instead.")
        num_threads = 1
    elif num_threads > max_threads:
        print(f"Too many threads. Max allowed is {max_threads}. Adjusting accordingly.")
        num_threads = max_threads

    print(f"Threads used  : {num_threads}\n")

    try:
        with open(wordlist_file, "r", encoding="unicode_escape") as file:
            passwords = file.readlines()
        total_passwords = len(passwords)
        print(f"Loaded {total_passwords} passwords to test")
    except FileNotFoundError:
        print(f"Wordlist not found: {wordlist_file}")
        return

    task_args = [(i, pw, db_file, keyfile_path) for i, pw in enumerate(passwords)]

    found_password = None
    start_time = time.time()
    total = 0

    # Create progress bar
    with tqdm(
        total=total_passwords, 
        desc="Testing passwords :D", 
        unit="pwd",
        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining} {postfix}]",
        postfix="0 pwd/sec"
    ) as pbar:
        
        with Pool(processes=num_threads) as pool:
            for i, result in enumerate(pool.imap_unordered(try_password, task_args)):
                pbar.update(1)
                elapsed = time.time() - start_time
                if elapsed > 0:
                    avg_speed = pbar.n / elapsed
                    pbar.set_postfix_str(f"{avg_speed:.1f} pwd/sec")
                
                if result:
                    found_password = result
                    pool.terminate()
                    break

    end_time = time.time()
    duration = end_time - start_time

    print("\nBrute-force finished.")
    print(f"Passwords tried : {total_passwords if found_password else pbar.n}")
    print(f"Time taken      : {duration:.2f} seconds")
    print(f"Speed           : {pbar.n/duration:.1f} passwords/second\n")

    if found_password:
        print(f"Password found: {found_password}")      
    else:
        print("No valid password found. ˙◠˙")

if __name__ == "__main__":
    main()
