import os
import pyautogui

##These two functions are used for formatting the os.popen() output.
def remove_str_data(string, data): #Data is a list
    for dat in data:
        try:
            string = string.replace(dat,  "")
        except:
            continue
    return string


def map_list_to_str(list_str):
    listToStr = ''.join(map(str, list_str))
    return listToStr

current_power_plan = ""

power_plans = {

}

def load_power_plans(): #This was more of a pain than expected...
    GUID_LEN = 36
    power_plans.clear()
    power_plans_unformatted = os.popen("powercfg /list").read().splitlines()[3::]
    power_plans_list = list()
    for power_plan in power_plans_unformatted:
        
        power_plan_edited = remove_str_data(power_plan, ["Power Scheme GUID: "])

        power_plans_list.append(power_plan_edited)
    
    for power_plan in power_plans_list:
        power_plans[remove_str_data(map_list_to_str(list(power_plan)[GUID_LEN+2::]), ["(", ")", "*", " "]).lower()] = map_list_to_str(list(power_plan)[0:GUID_LEN])


def gui_menu():

    for key in power_plans:
        if power_plans[key] in os.popen("powercfg /GetActiveScheme").read():
            current_power_plan = key

    keys = []
    for key in power_plans:
        keys.append(key)
    
    try:
        os.system(f"powercfg /setactive {power_plans[pyautogui.confirm(text=f'Current Power Plan: {current_power_plan}', title='Power Plan Menu', buttons=keys).lower()]}")

    except:
        pyautogui.alert(text="Failed to change your power config settings", title="Error", button='OK')

if __name__ == "__main__":
    load_power_plans()
    gui_menu()
