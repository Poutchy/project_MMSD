from libraries.paper import Paper

p1 = Paper(1, "Test", 10)
p2 = Paper(1, "Testo", 9)
p3 = Paper(2, "Testi", 11)
p4 = Paper(3, "Testa", 10)

print(p1 == p2)
print(p1 == p3)

print(p1 < p2)
print(p1 < p3)

print(p1 <= p2)
print(p1 <= p3)
print(p1 <= p4)
