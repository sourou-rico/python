fruits = [500, 75, 65, 82, 23]
def DistFif(fruit) : 
    return abs(fruit - 50)

fruits.sort(key=DistFif, reverse=True)
print(fruits)  # Tri des fruits par distance à 50