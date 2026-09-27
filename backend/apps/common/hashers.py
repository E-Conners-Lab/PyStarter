"""Argon2id parameters from the project's SEC-17 baseline."""
from django.contrib.auth.hashers import Argon2PasswordHasher


class LocalArgon2PasswordHasher(Argon2PasswordHasher):
    time_cost = 2
    memory_cost = 19456
    parallelism = 1
