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
	audio_strings = []
	controls_strings = []
	with open (in_put) as sett:
		lines = sett.readlines()
	
	# To Remove Comments and White Space
	lines = [i.strip() for i in lines]
	lines = [(i if i else "#") for i in lines]
	lines = [(settings_strings.append(i) if "#" not in i else i ) for i in lines]
	
	in_audio = False
	in_controls = False
	
	for i in settings_strings:
		if "Audio:" in i:
			in_audio = True
			in_controls = False
		
		if "Controls:" in i:
			in_audio = False
			in_controls = True
			
		if in_audio:
			audio_strings.append(i)
		
		elif in_controls:
			controls_strings.append(i)
	
	controls_settings = {}
	for j in controls_strings[1:]:
		control = [j.strip() for j in j.split(":")]
		controls_settings[control[0]] = make_to_QtKey(control[1])
	
	audio_settings = {}
	for k in audio_strings[1:]:
		audio = [k.strip() for k in k.split(":")]
		audio_settings[audio[0]] = float(audio[1]) if isnum(audio[1]) else audio[1]
	
	settings = {audio_strings[0].replace(":",""):audio_settings,controls_strings[0].replace(":",""):controls_settings}
	return settings
	
def settings_writer(settings_dict,output):
	with open(output, "w") as out:
		for key in settings_dict:
			out.write(key + ":\n\n")
			for lock in settings_dict[key]:
				out.write(lock + " : " + str(make_to_string(settings_dict[key][lock]) if type(settings_dict[key][lock]) == QtCore.Qt.Key or type(settings_dict[key][lock]) == QtCore.QKeyCombination else settings_dict[key][lock]) + "\n")
				
			out.write("\n\n")