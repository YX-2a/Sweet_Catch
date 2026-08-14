from PySide6 import QtCore, QtGui
from game_objects import Game_Sprite

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
	keys = {}
	with open (in_put) as sett:
		lines = sett.readlines()
	
	# To Remove Comments and White Space
	lines = [("#" if not i or i == "\n" else i) for i in lines]
	lines = [(settings_strings.append(i) if "#" not in i else i ) for i in lines]

	in_section = False
	section_nm = ""

	for i in settings_strings:
		if ":\n" in i:
			in_section = True
			section_nm = i[:-2]
			keys[section_nm] = {}
		elif " : " in i:
			knm = i.split(" : ")[0]
			val = i.split(" : ")[1].strip()
			if in_section:
				if isnum(val):
					keys[section_nm][knm] = float(val)

				elif section_nm == "Controls":
					keys[section_nm][knm] = make_to_QtKey(val)

				elif section_nm == "Audio":
					keys[section_nm][knm] = keys["Data_Dir"] + val

				elif section_nm == "Textures":
					keys[section_nm][knm] = Game_Sprite(keys["Data_Dir"] + val)
			else:
				in_section = False
				keys[knm] = val
	return keys
	
def settings_writer(settings_dict,output):
	with open(output, "w") as out:
		for key in settings_dict:
			if type(settings_dict[key]) == dict:
				for lock in settings_dict[key]:
					out.write(lock + " : " + str(make_to_string(settings_dict[key][lock]) if type(settings_dict[key][lock]) == QtCore.Qt.Key or type(settings_dict[key][lock]) == QtCore.QKeyCombination else settings_dict[key][lock]) + "\n")
			else:
				out.write(key + " : " + settings_dict[key] + "\n")
			out.write("\n\n")