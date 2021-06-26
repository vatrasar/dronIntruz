

def get_property_pair(property_line:str):

        index_of_equal =property_line.index("=")
        index_of_hash=2
        try:
            index_of_hash = property_line.index("#")
        except:
            index_of_hash=len(property_line)
        property_value = property_line[index_of_equal + 1:index_of_hash]
        property_name=property_line[:index_of_equal]
        return (property_name,property_value)

def check_binary(property_value,property_name):
    if (property_value == 1 or property_value == 0):
        if (property_value == 1):
            return True
        else:
            return False
    else:
        raise Exception("Błąd pliku konfiguracyjnego. %s może być 0 lub 1" % (property_name))

def check_float(property_value,property_name,min,max,no_max):
    if(no_max):
        if (property_value > min and property_value<max):
            return float(str(property_value))
        else:
            raise Exception("Błąd pliku konfiguracyjnego. %s musi być większe od %f" % (property_name,min))
    else:

        if (property_value > min and property_value<max):
            return float(str(property_value))
        else:
            raise Exception("Błąd pliku konfiguracyjnego. %s musi być pomiędzy %f i %f" % (property_name,min,max))

def check_int(property_value,property_name,min,max,no_max):
    if(no_max):
        if (property_value > min and property_value<max):
            return int(str(property_value))
        else:
            raise Exception("Błąd pliku konfiguracyjnego. %s musi być większe od %d" % (property_name,min))
    else:

        if (property_value > min and property_value<max):
            return int(str(property_value))
        else:
            raise Exception("Błąd pliku konfiguracyjnego. %s musi być pomiędzy %d i %d" % (property_name,min,max))

def get_properties():
    settings_file_name_f=open("settingsFileName.txt")
    settingsFileName_line:str=settings_file_name_f.readline()
    _,settingsFileName=get_property_pair(settingsFileName_line)
    file_with_properties=open(settingsFileName)
    setting_dict={}
    for record in file_with_properties.readlines():
        if(len(record)!=0):
            property_name,property_value=get_property_pair(record)
            property_value=check_property(property_name,property_value)

            setting_dict[property_name]=property_value

    return setting_dict

def check_property(property_name,property_value):

    if(property_name=="uav_number"):
        property_value=int(str(property_value))

        if(property_value>0 and property_value<=2):
            return property_value
        else:
            raise Exception("Błąd pliku konfiguracyjnego. %s może być tylko 1 lub 2"%(property_name))

    elif (property_name=="hands_number"):
        property_value = int(str(property_value))
        if (property_value >= 0 and property_value <= 2):
            return property_value
        else:
            raise Exception("Błąd pliku konfiguracyjnego. %s może być 0,1,2 "%(property_name))
    elif (property_name=="hands_number"):
        return check_binary(property_value,property_name)
    elif (property_name=="T"):
        return check_float(property_value,property_name,0,True)
    elif (property_name=="beat_the_score"):
        return check_float(property_value,property_name,0,1,True)

    elif (property_name=="intruder_max_energy"):
        return check_float(property_value,property_name,0,1,True)

    elif (property_name=="mode"):

        if (property_value=="RW-RA"):
            return property_value
        else:
            raise Exception("Błąd pliku konfiguracyjnego. %s może przyjmować wartości: RW-RA"%(property_name))

    elif (property_name=="prob_of_attack"):

        return check_float(property_value,property_name,0,1,False)
    elif (property_name=="prob_of_return_to_T2"):

        return check_float(property_value,property_name,0,1,False)

    elif (property_name=="arrive_deterministic"):

        return check_binary(property_value,property_name)
    elif (property_name=="arrive_deterministic"):

        return check_float(property_value,property_name,0,1,True)
    elif (property_name=="tier1_distance_from_intruder"):

        return check_float(property_value,property_name,0,1,True)

    elif (property_name=="v_of_uav"):

        return check_float(property_value,property_name,0,1,True)

    elif (property_name=="wiat_time"):

        return check_float(property_value,property_name,0,1,True)

    else:
        raise Exception("Błąd pliku konfiguracyjnego, nieznana nazwa właściwości:" +property_name)



