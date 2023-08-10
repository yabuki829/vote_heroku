import random, string

def create_string(n):
  """
    0-9,a_Zまでの文字列をランダムにn個出力します
  """
  randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
  return ''.join(randlst)