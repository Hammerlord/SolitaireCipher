from src.solitaire import generate_cards, encrypt, decrypt

input_key = generate_cards()
message = "If you can read this good for you"
encrypted = encrypt(input_key, message)
print(input_key)
print(encrypted)
print(decrypt(input_key, encrypted))
