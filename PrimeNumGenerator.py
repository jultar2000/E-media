from random import randrange, getrandbits


class PrimeNumGenerator:

    @staticmethod
    def rabin_miller_test(num, k=10):
        s = 0
        r = num - 1
        while r & 1 == 0:
            s += 1
            r //= 2

        for trials in range(k):
            a = randrange(2, num - 1)
            x = pow(a, r, num)
            if x != 1 and x != num - 1:
                j = 1
                while j < s and x != num - 1:
                    x = pow(x, 2, num)
                    if x == 1:
                        return False
                    j += 1
                if x != num - 1:
                    return False
        return True

    @staticmethod
    def is_prime(num, k):
        if num == 2 or num == 3:
            return True
        if num <= 1 or num % 2 == 0:
            return False

        return PrimeNumGenerator.rabin_miller_test(num, k)

    @staticmethod
    def generate_prime_candidate(length):
        prime_candidate = getrandbits(length)
        prime_candidate |= (1 << length - 1) | 1
        return prime_candidate

    @staticmethod
    def generate_prime_number(length=1024):
        prime = 4

        if not PrimeNumGenerator.is_prime(prime, k=10):
            prime = PrimeNumGenerator.generate_prime_candidate(length)
        return prime
