"""
This example shows how to write, read and manipulate value in storage.
It is also a good example of using neo-python's `debugstorage`, which
allows you to test `Put` operations with `build .. test` commands.
Debugstorage is enabled by default, you can disable it with
`debugstorage off` and, more importantly, reset it with
`debugstorage reset`.
Test & Build:
neo> build sc/3-storage.py test 07 05 True False
"""
from boa.interop.Neo.Storage import Get, Put, GetContext
from boa.interop.Neo.Runtime import Log, Notify, GetTrigger, CheckWitness

def Main(operation, args):
    # Am I who I say I am?
    user_hash = args[0]
    authorized = CheckWitness(user_hash)
    if not authorized:
        print("Not Authorized")
        return False
    print("Authorized")

