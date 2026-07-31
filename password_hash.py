from passlib.context import CryptContext


# bcrypt hashing setup
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# Original password
password = "mypassword123"


# Hash password
hashed_password = pwd_context.hash(password)

print("Hashed Password:")
print(hashed_password)


# Correct password verification
correct = pwd_context.verify(
    "mypassword123",
    hashed_password
)

print("Correct password:", correct)


# Wrong password verification
wrong = pwd_context.verify(
    "wrongpassword",
    hashed_password
)

print("Wrong password:", wrong)