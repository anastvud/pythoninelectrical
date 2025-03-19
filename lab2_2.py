l = list(map(int, input().split()))
l_transformed = list(map(lambda x: x**2, l))
l_filtered = list(filter(lambda x: x > 10, l_transformed))

print(l)
print(l_transformed)
print(l_filtered)
