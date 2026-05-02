simvols =  "+-/*!&$#?=@abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
generated_password = ""
password_len = int(input("Введите длину пароля: "))
for _ in range(password_len):
    random_char = random.choice(simvols)
    generated_password += random_char
print("Сгенерированный пароль:", generated_password)
