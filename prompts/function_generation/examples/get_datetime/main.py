import sys
import json

from get_datetime import get_datetime

if __name__ == "__main__":
  input_data = json.loads(sys.stdin.read())
  result = get_datetime(input_data)
  print(json.dumps(result))
