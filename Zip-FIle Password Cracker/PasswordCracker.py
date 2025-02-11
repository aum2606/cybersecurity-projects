import zipfile
import threading
from queue import Queue
import argparse
import time
from pathlib import Path
from typing import Optional, List
import logging

class PasswordCracker:
    def __init__(self,zip_file:str,wordlist_file:str,num_threads:int = 4):
        """initialize the zip file password cracker

        Args:
            zip_file (str): Path to the zip file
            wordlist_file (str): Path to the wordlist fiele
            num_threads (int, optional): Number of threads to use for cracking.
        """
        self.zip_file = zip_file
        self.wordlist_file = wordlist_file
        self.num_threads = num_threads
        self.password_queue = Queue()
        self.password_found = threading.Event()
        self.correct_password: Optional[str] = None
        # configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
    def load_wordlist(self) -> int:
        """load passwords from wordlist file into queue

        Returns:
            int: Number of passwords loaded
        """
        count = 0
        try:
            with open(self.wordlist_file,'r',encoding='utf-8',errors='ignore') as f:
                for line in f:
                    password = line.strip()
                    if password:
                        self.password_queue.put(password)
                        count += 1
            return count
        except Exception as e:
            self.logger.error(f"Error loading wordlist: {e}")
            raise
        
    def try_password(self,password:str)->bool:
        """try a password on the zip file
        Args:
            password (str): Password to try
        Returns:
            bool: True if password is correct, False otherwise
        """
        try:
            with zipfile.ZipFile(self.zip_file) as zf:
                zf.extractall(pwd = password.encode())
                return True
        except:
            return False
        
    def password_cracker_worker(self):
        """worker threads that attempts passwords from the queue"""
        while not self.password_found.is_set() and not self.password_queue.empty():
            password = self.password_queue.get()
            self.logger.debug(f"Trying password:  {password}")

            if self.try_password(password):
                self.correct_password = password
                self.password_found.set()
                self.logger.info(f"Password found: {password}")
                break
            self.password_queue.task_done()
            
    def crack(self)-> Optional[str]:
        """Start the password cracking process
        Returns:
            Optional[str]: The correct password, or None if the process was cancelled
        """
        if not Path(self.zip_file).exists():
            raise FileNotFoundError(f"ZIP file not found: {self.zip_file}")
        
        if not Path(self.wordlist_file).exists():
            raise FileNotFoundError(f"Wordlist file not found: {self.wordlist_file}")
        
        #load passwords
        total_passwords = self.load_wordlist()
        self.logger.info(f"loaded{total_passwords} passwords from wordlist")
        
        #create and start worker threads
        threads: List[threading.Thread] = []
        start_time = time.time()
        
        for _ in range(self.num_threads):
            thread = threading.Thread(target=self.password_cracker_worker)
            thread.daemon = True
            thread.start()
            threads.append(thread)
            
        # wait for password to be found or queue to be empty
        for thread in threads:
            thread.join()
            
        end_time = time.time()
        duration = end_time - start_time
        
        if self.correct_password:
            self.logger.info(f"Cracking completed in {duration:.2f} seconds")
            return self.correct_password
        else:
            self.logger.info("Password not found in wordlist")
            return None
                        
                        
                        