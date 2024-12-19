import base64
from app.main import Application

Application = Application()

public, private = Application.security.generate_rsa_keys(2048)
message = "WissemLPlusBeau"
print("Message: ", message)
print("Public key: ", public)
encrypted = Application.security.encrypt.RSA(message, public)

private_key = [
                base64.b64encode(Application.security.manager.double_decrypt(base64.b64decode(private[0].encode("utf-8")))),
                base64.b64encode(Application.security.manager.double_decrypt(base64.b64decode(private[1].encode("utf-8"))))
               ]

print(Application.security.decrypt.RSA(encrypted, private_key))

