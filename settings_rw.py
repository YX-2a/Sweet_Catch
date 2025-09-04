from PySide6 import QtCore

def isnum(string):
    try:
        val = float(string)
        return True
    except Exception:
        return False

def make_to_QtKey(string):
	final_stuff = ""
	if "+" in string:
		mod_list = ["Control", "Shift", "Meta", "Alt"]
		final_stuff += "QtCore.QKeyCombination("
		string = [i.strip() for i in string.split("+")]
		for key in string:
			if key in mod_list:
				final_stuff += "QtCore.Qt." + key + "Modifier" + ("|" if string[string.index(key) + 1] in mod_list else ",")
			else:
				final_stuff += "QtCore.Qt.Key_" + key + ")"
	else:
		final_stuff += "QtCore.Qt.Key_" + string
	
	return eval(final_stuff)
	
def make_to_string(QtKey):
	if type(QtKey) == QtCore.Qt.Key:
		return QtKey.name.replace("Key_","")
		
	else:
		result_str = QtKey.keyboardModifiers().name
		if "|" in result_str:
			result_str = result_str.replace("|"," + ")
			
		return result_str.replace("Modifier","") + " + " + QtKey.key().name.replace("Key_","")

def settings_reader(in_put):
	settings_strings = []
	with open (in_put) as sett:
		lines = sett.readlines()
	lines = [i.strip() for i in lines]
	lines = [(i if i else "#") for i in lines]
	lines = [(settings_strings.append(i) if "#" not in i else i ) for i in lines]
	settings = {[j.strip() for j in i.split(":")][0]:(float([j.strip() for j in i.split(":")][1]) if isnum([j.strip() for j in i.split(":")][1]) else make_to_QtKey([j.strip() for j in i.split(":")][1])) for i in settings_strings}
	return settings
	
def settings_writer(settings_dict,output):
	with open(output, "w") as out:
		for key in settings_dict:
			out.write(key + " : " + (str(settings_dict[key])  if type(settings_dict[key]) == float else make_to_string(settings_dict[key])) + "\n")
			