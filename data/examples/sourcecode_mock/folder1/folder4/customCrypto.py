from django.contrib.auth.hashers import BasePasswordHasher

class CustomPasswordHasher(BasePasswordHasher):
    algorithm = "custom_hasher"
    def encode(self, password, salt):
        assert salt is not None
        return f'{salt}${password}'

    def verify(self, password, encoded):
        salt, hashed_password = encoded.split('$', 1)
        return self.encode(password, salt) == encoded

    def safe_summary(self, encoded):
        return {
            'algorithm': self.algorithm,
            'salt': encoded.split('$', 1)[0],
        }
