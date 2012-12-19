def map_value(val, in_min, in_max, out_min, out_max):
   result = (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min 
   return result