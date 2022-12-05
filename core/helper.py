from rest_framework.exceptions import ValidationError

def check_premium(paid, is_premium):
    """ 
    returns true if paid is true and ispremium is true.
    else raises exception
     """
    if paid is True and is_premium is True:
        return True
    
    if paid is True and is_premium is False:
        raise ValidationError({'error': 'premium must be True is paid is True'})
    
    if paid is False and is_premium is True:
        raise ValidationError({'error': 'paid must be True is premium is True'})

    return False