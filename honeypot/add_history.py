import pickle, time

A_NAME, A_TYPE, A_UID, A_GID, A_SIZE, A_MODE, A_CTIME, A_CONTENTS = range(8)
T_DIR, T_FILE = 1, 2

HIST = "honeypot/honeyfs/root/.bash_history"
OLD, NEW = b"svr04", b"mku-webserver-01"
OLD_TS = 1718100000  # 2024-06-11

OSREL = (
    b'PRETTY_NAME="Debian GNU/Linux 12 (bookworm)"\n'
    b'NAME="Debian GNU/Linux"\n'
    b'VERSION_ID="12"\n'
    b'VERSION="12 (bookworm)"\n'
    b'VERSION_CODENAME=bookworm\n'
    b'ID=debian\n'
    b'HOME_URL="https://www.debian.org/"\n'
    b'SUPPORT_URL="https://www.debian.org/support"\n'
    b'BUG_REPORT_URL="https://bugs.debian.org/"\n'
)

data = open(HIST, "rb").read().replace(b"\r\n", b"\n")

with open("honeypot/fs.pickle", "rb") as f:
    try:
        fs = pickle.load(f)
    except UnicodeDecodeError:
        f.seek(0)
        fs = pickle.load(f, encoding="utf8")

# --- .bash_history ---
root = next(c for c in fs[A_CONTENTS] if c[A_NAME] == "root")
node = next((c for c in root[A_CONTENTS] if c[A_NAME] == ".bash_history"), None)

if node:
    node[A_CONTENTS] = data
    node[A_SIZE] = len(data)
else:
    root[A_CONTENTS].append(
        [".bash_history", T_FILE, 0, 0, len(data), 0o100600, OLD_TS, data, None, None]
    )
    node = root[A_CONTENTS][-1]
node[A_CTIME] = OLD_TS

# --- hostname scrub ---
def scrub(n, path):
    if n[A_TYPE] == T_DIR:
        for c in n[A_CONTENTS]:
            scrub(c, path + "/" + c[A_NAME])
    elif n[A_TYPE] == T_FILE and isinstance(n[A_CONTENTS], bytes) and OLD in n[A_CONTENTS]:
        n[A_CONTENTS] = n[A_CONTENTS].replace(OLD, NEW)
        n[A_SIZE] = len(n[A_CONTENTS])
        print("scrubbed hostname in:", path)

scrub(fs, "")

# --- /etc/os-release ---
etc = next(c for c in fs[A_CONTENTS] if c[A_NAME] == "etc")
osr = next((c for c in etc[A_CONTENTS] if c[A_NAME] == "os-release"), None)
print("os-release before:", None if osr is None else (osr[:7], type(osr[A_CONTENTS]).__name__, osr[8]))
if osr:
    osr[A_TYPE] = T_FILE
    osr[A_CONTENTS] = OSREL
    osr[A_SIZE] = len(OSREL)
    osr[8] = None
else:
    etc[A_CONTENTS].append(
        ["os-release", T_FILE, 0, 0, len(OSREL), 0o100644, OLD_TS, OSREL, None, None]
    )

with open("honeypot/fs.custom.pickle", "wb") as f:
    pickle.dump(fs, f)

print("/root now contains:", [c[A_NAME] for c in root[A_CONTENTS]])

