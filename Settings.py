

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
        if (property_value ==1 or property_value == 0):
            if(property_value==1):
                return True
            else:
                return False
        else:
            raise Exception("Błąd pliku konfiguracyjnego. %s może być 0 lub 1"%(property_name))
    elif (property_name=="T"):
        if (property_value>0):
            return float(str(property_value))
        else:
            raise Exception("Błąd pliku konfiguracyjnego. %s musi być większa niż 0"%(property_name))
    elif (property_name=="beat_the_score"):
        property_value = int(str(property_value))
        if (property_value>0):
            return property_value
        else:
            raise Exception("Błąd pliku konfiguracyjnego. %s musi być większa niż 0"%(property_name))

    elif (property_name=="intruder_max_energy"):
        property_value = int(str(property_value))
        if (property_value>0):
            return property_value
        else:
            raise Exception("Błąd pliku konfiguracyjnego. %s musi być większa niż 0"%(property_name))

    else:
        raise Exception("Błąd pliku konfiguracyjnego, nieznana nazwa właściwości:" +property_name)



