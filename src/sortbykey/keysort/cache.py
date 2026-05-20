import logging
import sqlite3 as sql
import sortbykey.fs as fs
from collections import namedtuple
from pathlib import Path
from xxhash import xxh64
from typing import Tuple
from time import time as time_s
from sortbykey.analyzer import SUPPORTED_FILETYPES

def now() -> int:
    return int(time_s())

class HashDB:

    def __init__(self, output_path: Path):
        self.__directory = output_path.resolve()
        cache_path = self.directory / ".cache"
        # Ensure cache directory exists
        cache_path.mkdir(parents=True, exist_ok=True)
        # Connect to database in cache directory, creating it if it doesn't exist.
        database_file = cache_path / "sortbykey.db" 
        self.__con = sql.connect(database=database_file)
        self.__cur = self.__con.cursor()
    
    @property
    def directory(self):
        return self.__directory

    def close(self):
        self.__con.close()
    
    def __del__(self):
        # Ensure we close our connection when we die.
        self.close()

    def initialize_table(self) -> bool:
        '''
        :brief: Create the cache table, if it doesn't exist already.
        If it doesn't exist, create the table SortByKeyCache of format:
            filename TEXT PRIMARY KEY
            hash BLOB
            last_touched INTEGER

        :return: True if creation succeeds, False otherwise.
        :rtype: bool
        '''
        create_cache_table = """
        CREATE TABLE IF NOT EXISTS SortByKeyCache (
            filename TEXT PRIMARY KEY,
            hash BLOB,
            last_touched INTEGER
        );
        """
        try:
            self.__cur.execute(create_cache_table)
            self.commit()
        except Exception as ex:
            logging.error("Error creating hash table: %s", ex)
            return False
        else:
            return True

    def commit(self) -> bool:
        '''
        Commit changes to the database.

        :return: True if commit succeeds, False otherwise.
        :rtype: bool
        '''
        try:
            self.__con.commit()
        except Exception as ex:
            logging.error("Error committing changes to hash table: %s", ex)
            return False
        else:
            return True
    
    def hash_file(self, filepath: Path, *, chunk_size: int = 1024 * 1024) -> bytes:
        '''
        Hash a file according to the hashing algorithm.

        :param filepath: Path of file to hash.
        :type filepath: Path
        :param chunk_size: Size of chunks, in bytes, to read of file. Defaults to 1 MB (1048576).
        :type chunk_size: int, Optional
        :return: A hash digest, in bytes, of the file.
        :rtype: bytes
        '''
        path = filepath.resolve()
        hasher = xxh64()
        with open(path, "rb") as file:
            while data := file.read(chunk_size):
                hasher.update(data)
        return hasher.digest()
    
    def add_hash(self, filename:str, hash: bytes) -> bool:
        '''
        Add a hash to the database.

        :param filename: Path of the file the hash belongs to.
        :type filename: str
        :param hash: The hash digest, in bytes, of the file.
        :type hash: bytes
        :raises TypeError: hash is not type bytes
        :raises ValueError: hash is larger or smaller than expected digest size
        :raises TypeError: filename is not type str
        :return: True if adding succeeds, False otherwise
        :rtype: bool
        '''
        if not isinstance(hash, bytes):
            raise TypeError(f"\"{hash=!r}\" must be type bytes, not type \"{hash.__class__.__name__}\"")
        if len(hash) != 8:
            raise ValueError(f"\"{hash=!r}\" must be length 8, not {len(hash)}.")
        if not isinstance(filename, str):
            raise TypeError(f"\"{filename=!r}\" must be type str, not type \"{filename.__class__.__name__}\"")
        try:
            stmnt = """
                INSERT INTO SortByKeyCache VALUES
                    (:filename, :hash, :touched);
            """
            self.__cur.execute(stmnt, {"filename": filename, "hash": hash, "touched": now()})
        except Exception as ex:
            logging.error("Error adding hash to hash table: %s", ex)
            return False
        else:
            return True

    def add_file(self, filepath: Path) -> bool:
        '''
        Add a file to the database, hashing as needed.

        :param filepath: Path of the file to add to the database.
        :type filepath: Path
        :return: True if adding file succeeds, False otherwise.
        :rtype: bool
        '''
        path = filepath.resolve()

        return self.add_hash(str(path), self.hash_file(filepath))
    
    def remove_hash(self, hash: bytes) -> bool:
        '''
        Remove a hash from the database.

        :param hash: Hash to remove from the database.
        :type hash: bytes
        :raises TypeError: If hash is not type bytes.
        :return: True if removal succeeds, False otherwise.
        :rtype: bool
        '''
        if not isinstance(hash, bytes):
            raise TypeError(f"\"{hash=!r}\" must be type bytes, not type \"{hash.__class__.__name__}\"")
        try:
            stmnt = """
                DELETE FROM SortByKeyCache WHERE
                    hash = :hash;
            """
            self.__cur.execute(stmnt, {"hash": hash})
        except Exception as ex:
            logging.error("Error removing hash from hash table: %s", ex)
            return False
        else:
            return True
    
    def remove_file(self, filepath: Path) -> bool:
        '''
        Remove a file from the database.

        :param filepath: Path of the file to remove.
        :type filepath: Path
        :raises TypeError: filepath is not a Path
        :return: True if removal succeeds, False otherwise.
        :rtype: bool
        '''
        if not isinstance(file, Path):
            raise TypeError(f"\"{file=!r}\" must be type pathlib.Path, not type \"{file.__class__.__name__}\"")
        path = filepath.resolve()
        try:
            stmnt = """
                DELETE FROM SortByKeyCache WHERE
                    filename = :filename;
            """
            self.__cur.execute(stmnt, {"filename": str(path)})
        except Exception as ex:
            logging.error("Error removing file from hash table: %s", ex)
            return False
        else:
            return True
    
    
    def lookup_hash(self, hash: bytes) -> Tuple | None:
        '''
        Get a hash from the database, assuming it has one.

        :param hash: Hash to lookup
        :type hash: bytes
        :raises TypeError: hash is not type bytes
        :return: Tuple from database, or None if not in the database.
        :rtype: Tuple | None
        '''
        if not isinstance(hash, bytes):
            raise TypeError(f"\"{hash=!r}\" must be type bytes, not type \"{hash.__class__.__name__}\"")
        try:
            stmnt = """
                SELECT 
                    *
                FROM SortByKeyCache 
                WHERE
                    hash = :hash;
            """
            self.__cur.execute(stmnt, {"hash": hash})
            results = self.__cur.fetchone()
        except Exception as ex:
            logging.error("Error selecting hash from hash table: %s", ex)
            return False
        else:
            return results

    def lookup_filepath(self, filepath: Path) -> Tuple | None:
        '''
        Lookup a filepath in the database.

        :param filepath: Path of file to lookup.
        :type filepath: Path
        :raises TypeError: filepath is not type pathlib.Path
        :return: Tuple if record exists in database, None otherwise.
        :rtype: Tuple | None
        '''
        if not isinstance(filepath, Path):
            raise TypeError(f"\"{filepath=!r}\" must be type pathlib.Path, not type \"{filepath.__class__.__name__}\"")
        path = filepath.resolve()
        try:
            stmnt = """
                SELECT 
                    *
                FROM SortByKeyCache 
                WHERE
                    filename = :filename;
            """
            self.__cur.execute(stmnt, {"filename": str(path)})
            results = self.__cur.fetchone()
        except Exception as ex:
            logging.error("Error selecting file from hash table: %s", ex)
            return False
        else:
            return results
    
    def update_file(self, filepath: Path) -> bool:
        '''
        Refresh a file in the database with an updated hash.

        :param filepath: Path of file to update.
        :type filepath: Path
        :raises TypeError: filepath is not type pathlib.Path
        :return: True if update succeeds, False otherwise.
        :rtype: bool
        '''
        if not isinstance(filepath, Path):
            raise TypeError(f"\"{filepath=!r}\" must be type pathlib.Path, not type \"{filepath.__class__.__name__}\"")
        path = filepath.resolve()
        filehash = self.hash_file(path)
        try:
            stmnt = """
                UPDATE SortByKeyCache 
                SET
                    hash = :hash,
                    last_touched = :now
                WHERE
                    filename = :filename;
            """
            self.__cur.execute(stmnt, {"filename": str(path), "hash": filehash, "now": now()})
        except Exception as ex:
            logging.error("Error updating file from hash table: %s", ex)
            return False
        else:
            return True

    def has_hash(self, hash: bytes) -> bool:
        '''
        Check if database contains a hash.

        :param hash: Hash to lookup.
        :type hash: bytes
        :return: True if database contains hash, False otherwise.
        :rtype: bool
        '''
        results = self.lookup_hash(hash)
        if results is None:
            return False
        if not results:
            return False
        return True
    
    def lookup_file_by_hash(self, filepath: Path) -> Tuple | None:
        '''
        Lookup a file by it's hash, returning the resulting row if it exists.

        :param filepath: Path of file to check.
        :type filepath: Path
        :return: The resulting row in the database if it exists.
        :rtype: Tuple | None
        '''
        filehash = self.hash_file(filepath)
        return self.lookup_hash(filehash)

    def update(self, stale_threshold: int = 60 * 60 * 24 * 7):
        '''
        Read through directory and update the database as necessary,
        adding files if they don't exist and updating them if they're too stale.

        :param stale_threshold: How old a file needs to be, in integer seconds, to be considered "stale"; defaults to one week (604800)
        :type stale_threshold: int, optional
        '''
        # Step 1: Remove any nonexistent files from the database.
        select_stmt = """
        SELECT 
            filename
        FROM SortByKeyCache
        """
        self.__cur.execute(select_stmt)
        db_filenames = self.__cur.fetchall()
        for row in db_filenames:
            db_filename = row[0]
            db_path = Path(db_filename).resolve()
            # If file exists, continue to the next one.
            if db_path.exists():
               continue
            self.remove_file(db_path)
        self.commit()
        # Step 2: Add/update all existing files.
        for root, filename in fs.traverse(self.directory, filetype_filter=SUPPORTED_FILETYPES):
            filepath = (root / filename).resolve()
            db_file = self.lookup_filepath(filepath)
            if db_file is None:
                # File doesn't exist; add it.
                self.add_file(filepath)
                self.commit()
                continue
            timestamp = db_file[2]
            diff = (timestamp - now())
            if diff < stale_threshold:
                # File isn't stale yet; don't touch it.
                continue
            # File is stale; update it.
            self.update_file(filepath)
            self.commit()

