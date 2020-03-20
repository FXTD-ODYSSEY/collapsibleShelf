import sys
MODULE = r"C:\Users\timmyliang\Desktop\repo\collapsibleShelf\scripts"
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