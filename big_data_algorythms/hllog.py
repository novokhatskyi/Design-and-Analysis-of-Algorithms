import random
import mmh3
import math

class HyperLogLog:
    def __init__(self, p=5):
        if not (4 <= p <= 16):
            raise ValueError("p повинно бути в діапазоні від 4 до 16 для 32-бітного хешу")
        self.p = p
        self.m = 1 << p
        self.registers = [0] * self.m
        self.alpha = self._get_alpha()
        self.small_range_correction = 2.5 * self.m  # Стандартний поріг 2.5 * m

    def _get_alpha(self):
        # Точні коефіцієнти з оригінальної статті Flajolet
        if self.m == 16:
            return 0.673
        elif self.m == 32:
            return 0.697
        elif self.m == 64:
            return 0.709
        else:
            return 0.7213 / (1.0 + 1.079 / self.m)

    def add(self, item):
        x = mmh3.hash(str(item), signed=False)
        j = x & (self.m - 1)          # Перші p бітів для індексу
        w = x >> self.p               # Решта бітів для підрахунку нулів
        
        self.registers[j] = max(self.registers[j], self._rho(w))

    def _rho(self, w):
        """Повертає позицію першої одиниці (кількість нулів з права + 1)"""
        if w == 0:
            # Максимально можлива кількість нулів + 1 для залишку бітів
            return (32 - self.p) + 1
        
        # Швидкий спосіб знайти кількість нулів з правого боку в бінарному числі
        # (w & -w) виділяє наймолодший біт. math.log2 знаходить його індекс.
        return int(math.log2(w & -w)) + 1

    def count(self):
        Z = sum(2.0 ** -r for r in self.registers)
        E = self.alpha * (self.m ** 2) / Z
        
        # Корекція для малих значень (Linear Counting)
        if E <= self.small_range_correction:
            V = self.registers.count(0)
            if V > 0:
                return self.m * math.log(self.m / V)
        
        return E

# Приклад використання
hll = HyperLogLog(p=16) # p=16 дає 65,536 регістрів (хороша точність)

# Всього 20 унікальних тегів
all_tags = ["python", "fastapi", "web", "api", "database", "sql", "orm", "async",
            "programming", "coding", "development", "software", "tech", "data",
            "backend", "frontend", "fullstack", "learning", "tutorial", "blog"]

# Додаємо їх 100 000 разів (унікальних все одно залишається 20!)
for i in range(100000):
    hll.add(random.choice(all_tags))

estimated_cardinality = hll.count()
print(f"Реальна кількість унікальних елементів: {len(all_tags)}")
print(f"Оцінена кардинальність: {round(estimated_cardinality, 2)}")