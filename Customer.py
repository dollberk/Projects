import string
import random
import csv
from datetime import datetime, timedelta

random.seed(123)
customer_id = []
baker_id = []
wedding_order = []
icing_flavor = []
filling_flavor = []
cake_flavor = []
tier_id = []


def write_customers():

    customer = []
    fields = ['CustomerID', 'Name', 'Address', 'Phone']

    for i in range(10000):
        letters = string.ascii_lowercase

        name = ''.join(random.choice(letters) for j in range(20))
        address = str(random.randint(1, 9999)) + ' ' + ''.join(random.choice(letters) for k in range(20))
        phone = random.randint(1111111111, 9999999999)
        customer_id.append(i)
        customer.append((i, name, address, phone))

    with open('CustomerData.txt', 'w') as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(customer)

    return customer_id


def write_baker():

    baker = []
    fields = ['employeeID', 'employeeName', 'Salary', 'yearsExperience']

    for i in range(1000):
        letter = string.ascii_lowercase

        name = ''.join(random.choice(letter) for j in range(20))
        salary = random.randint(10000, 100000)
        years_ex = random.randint(1, 20)
        baker_id.append(i + 100)
        baker.append((i + 100, name, salary, years_ex))

    with open('BakerData.txt', 'w') as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(baker)

    return baker_id


def write_wedding_order():

    order = []
    fields = ['orderID', 'customerID', 'employeeID', 'numTiers', 'difficulty', 'orderedDate', 'deliveryDate', 'price']

    for i in range(75000):
        customer = random.choice(customer_id)
        employee = random.choice(baker_id)
        tiers = random.randint(1, 10)
        difficulty = random.randint(1, 20)

        start = datetime(2000, 1, 1, 00, 00, 00)
        end = start + timedelta(days=365 * 21)

        ordered = start + (end - start) * random.random()
        delivery = ordered + timedelta(days=random.randint(10, 100))
        price = tiers * 300
        wedding_order.append(i + 100000)
        order.append((i + 100000, customer, employee, tiers, difficulty, ordered, delivery, price))

    with open('WeddingCakeData.txt', 'w') as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(order)

    return wedding_order


def write_icing():

    icing = []
    fields = ['icingFlavor', 'color', 'price']
    colors = 'red', 'white', 'yellow', 'black', 'blue', 'green', 'ivory', 'pink', 'orange', 'purple', 'brown'
    for i in range(50):
        letter = string.ascii_lowercase

        flavor = ''.join(random.choice(letter) for j in range(5))
        color = random.choice(colors)
        price = round(random.uniform(0.01, 10.00), 2)
        icing_flavor.append(flavor)
        icing.append((flavor, color, price))

    with open('IcingData.txt', 'w') as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(icing)

    return icing_flavor


def write_filling():

    filling = []
    fields = ['fillingFlavor', 'price']
    for i in range(15):
        letter = string.ascii_lowercase

        flavor = ''.join(random.choice(letter) for j in range(5))
        price = round(random.uniform(0.01, 30.00), 2)
        filling_flavor.append((flavor, price))
        filling.append((flavor, price))

    with open('FillingData.txt', 'w') as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(filling)

    return filling_flavor


def write_cake():

    cake = []
    fields = ['cakeFlavor', 'fillingFlavor', 'price']
    for i in range(60):
        letter = string.ascii_lowercase
        filling, fprice = random.choice(filling_flavor)
        print(filling)
        flavor = ''.join(random.choice(letter) for j in range(10))
        price = round(random.uniform(0.01, 30.00) + fprice, 2)
        cake_flavor.append((flavor, price))
        cake.append((flavor, filling, price))

    with open('CakeData.txt', 'w') as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(cake)

    return cake_flavor


def write_tier():

    tier = []
    fields = ['tierID', 'orderID', 'icingFlavor', 'cakeFlavor', 'size', 'shape']
    for i in range(300):
        shapes = 'circle', 'square', 'rectangle', 'heart', 'octagon', 'diamond', 'oval', 'other'

        order = random.choice(wedding_order)
        icing = random.choice(icing_flavor)
        cake, cprice = random.choice(cake_flavor)
        size = random.randint(5, 24)
        shape = random.choice(shapes)
        tier_id.append(i + 1000)
        tier.append((i + 1000, order, icing, cake, size, shape))

    with open('TierData.txt', 'w') as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(tier)

    return tier_id


if __name__ == "__main__":
    write_customers()
    write_baker()
    write_wedding_order()
    write_icing()
    write_filling()
    write_cake()
    write_tier()
