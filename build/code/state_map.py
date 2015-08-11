# -*- coding: utf-8 -*-

def build():
    
    state_list = ['AL', 'AZ', 'AR', 'CA', 'CO',\
                'CT', 'DE', 'FL', 'GA', 'ID',\
                'IL', 'IN', 'IA', 'KS', 'KY',\
                'LA', 'ME', 'MD', 'MA', 'MI',\
                'MN', 'MS', 'MO', 'MT', 'NE',\
                'NV', 'NH', 'NJ', 'NM', 'NY',\
                'NC', 'ND', 'OH', 'OK', 'OR',\
                'PA', 'RI', 'SC', 'SD', 'TN',\
                'TX', 'UT', 'VT', 'VA', 'WA',\
                'WV', 'WI', 'WY']

    state_map = {}
    
    for item in state_list:
        
        value = state_list.index(item) + 1
        
        if value <= 9:
            
            value_string = '0' + str(value)
            
        else:
            
            value_string = str(value)
            
        state_map[item] = value_string
    
    return state_map
