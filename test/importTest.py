import sys
MODULE = r"D:\Users\82047\Desktop\repo\collapsibleShelf\scripts"
# MODULE = r"C:\Users\timmyliang\Desktop\repo\collapsibleShelf\scripts"
if MODULE not in sys.path:
    sys.path.append(MODULE)

import collapsibleShelf
# reload(collapsibleShelf)
try:
    collapsibleShelf.install()
except:
    import traceback
    traceback.print_exc()

# collapsibleShelf.uninstall()