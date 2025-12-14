import bcrypt
import os
import subprocess

class SystemLogic:
    @staticmethod
    def hash_password(plain_password):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(plain_password.encode('utf-8'), salt)

    @staticmethod
    def check_password(plain_password, hashed_password):
        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode('utf-8')
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

    @staticmethod
    def lock_folder(path):
        try:
            os.system(f'attrib +h +s "{path}"')
            subprocess.run(['icacls', path, '/deny', 'Everyone:(OI)(CI)F'], creationflags=0x08000000) 
            return True
        except Exception as e:
            print(f"Error locking: {e}")
            return False

    @staticmethod
    def unlock_folder(path):
        try:
            subprocess.run(['icacls', path, '/remove:d', 'Everyone'], creationflags=0x08000000)
            os.system(f'attrib -h -s "{path}"')
            return True
        except Exception as e:
            print(f"Error unlocking: {e}")
            return False