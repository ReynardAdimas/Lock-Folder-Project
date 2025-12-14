import bcrypt
import os
import subprocess

class SystemLogic:
    @staticmethod
    def hash_password(plain_password):
        # Mengubah password text menjadi hash
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(plain_password.encode('utf-8'), salt)

    @staticmethod
    def check_password(plain_password, hashed_password):
        # Mencocokkan input user dengan hash di database
        # hashed_password dari DB biasanya string, perlu di encode ke bytes
        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode('utf-8')
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

    @staticmethod
    def lock_folder(path):
        # Logika mengunci folder di Windows
        try:
            # 1. Hidden & System attribute
            os.system(f'attrib +h +s "{path}"')
            # 2. Deny Access (Butuh Run as Admin)
            # /deny Everyone:(OI)(CI)F -> Object Inherit, Container Inherit, Full Control
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