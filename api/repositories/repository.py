from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one():
        """ Creates new row in database """
        raise NotImplementedError

    @abstractmethod
    async def find_all():
        """ Returns all rows from database or None if its no one row in db """
        raise NotImplementedError

    @abstractmethod
    async def find_one():
        """ Returns one row from database or error if query object doesnt exist"""
        raise NotImplementedError

    @abstractmethod
    async def update_one():
        """ 
        Updated one row from database and returns new object or error 
        if query object doesnt exist 
        """
        raise NotImplementedError

    @abstractmethod
    async def delete_one():
        """ Deletes one row from database and returns 200 status or error if query object doesnt exist """
        raise NotImplementedError
