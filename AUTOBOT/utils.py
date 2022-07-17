import base64


async def encode(stri):
  stri = stri.encode("ascii")
  stri = base64.b64encode(stri)
  stri = stri.decode("ascii")
  return stri

async def decode(stri):
  stri = stri.encode("ascii")
  stri = base64.b64decode(stri)
  stri = stri.decode("ascii")
  return stri

  
async def get_ids(strt, end):
  ids = []
  for a in range(end - strt +1):
    id = strt + a
    ids.append(int(id))
  return ids