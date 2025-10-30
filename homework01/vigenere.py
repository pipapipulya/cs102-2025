def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    key_index = 0
    for ch in plaintext:
        key_char = keyword[key_index % len(keyword)]
        shift = ord(key_char.lower()) - ord("a")
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            cipher_char = chr((ord(ch) - base + shift) % 26 + base)
        else:
            cipher_char = ch
        ciphertext += cipher_char
        key_index += 1
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    key_index = 0
    for ch in ciphertext:
        key_char = keyword[key_index % len(keyword)]
        shift = ord(key_char.lower()) - ord("a")
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            plain_char = chr((ord(ch) - base - shift) % 26 + base)
        else:
            plain_char = ch
        plaintext += plain_char
        key_index += 1
    return plaintext
