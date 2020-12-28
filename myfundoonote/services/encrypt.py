import jwt
from decouple import config


class Encrypt:
    """
    Created a class to encode and decode a token

    """
    @staticmethod
    def decode(token):
        """
        Created a method to decode a token

        Args:
            token : encoded token is sent by user

        Returns:
            id: id of the user to verify the user to have access
        """
        return jwt.decode(token, config('ENCODE_SECRET_KEY'), algorithms=["HS256"])

    @staticmethod
    def encode(user_id):
        """[summary]

        Args:
            user_id : the user id of the respective user

        Returns:
            token: stringified encoded token to store in redis cache
        """
        return jwt.encode({"id": user_id}, config('ENCODE_SECRET_KEY'), algorithm="HS256").decode('utf-8')