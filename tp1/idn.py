import time

from rigol import Generator, Scope

gen = Generator()
scope = Scope()
gen.connect()
scope.connect()

gen.write("*IDN?")
scope.write("*IDN?")
time.sleep(1)  # no query(): give the instruments time to reply
print("Generator:", gen.read())
print("Scope    :", scope.read())
