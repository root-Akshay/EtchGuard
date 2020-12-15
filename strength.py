def strong(input_string): 
      
    n = len(input_string)  
  
  
    hasLower = False
    hasUpper = False
    hasDigit = False
    specialChar = False
    normalChars = "abcdefghijklmnopqrstu"
    "vwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 "
      
    for i in range(n): 
        if input_string[i].islower(): 
            hasLower = True
        if input_string[i].isupper(): 
            hasUpper = True
        if input_string[i].isdigit(): 
            hasDigit = True
        if input_string[i] not in normalChars: 
            specialChar = True
  
    if (hasLower and hasUpper and 
        hasDigit and specialChar and n >= 8): 
        return "Strong" 
          
    elif ((hasLower or hasUpper) and 
          specialChar and n >= 6): 
        return "Moderate"
    else: 
        return "Weak"