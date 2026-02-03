
# a = input("enter an integer: ") # how to make sure input is integer
# a = int(a)
# print(type(a))

# # check odd or even
# if a % 2 ==0:
#     print("Even")
# else:
#     print("Odd")
#     """

# """
# # a product would cost $100, how much tax do we pay?
# product = 100 # unit = dollars
# taxRate = 0.0625
# tax = product * taxRate
# print(f'The tax for the product which costs #{product} is #{tax}.') #The f is formatted printing


computerPrice = 900
iPhonePrice = 1100

def calc_tax(price, taxRate):
    """Calculate product tax based on given price"""
    tax = price * taxRate
    #print(f'The tax for the product which costs #{product} is #{tax}.') 
    #print(tax)
    # if the function does not explicitly return any value, it would return None
    #return None
    return tax # RETURN Tax, rather than just printing it
#calc_tax(100)
#calc_tax(20)

taxRate = 0.0625
massTaxRate = 0.0625
nyTaxRate = 8.875 / 100
total_tax = calc_tax(computerPrice, massTaxRate) + calc_tax(iPhonePrice, massTaxRate)
print(total_tax)