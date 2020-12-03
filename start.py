import PySimpleGUI as sg

sg.theme('DarkAmber')

layout_resolve_creatives = []

layout_dynamic_targeting_key = [
	[sg.Text('Url of filtered creatives in CM: '), sg.InputText()],
    [sg.Text('Dynamic targeting keys seperate by (,): '), sg.InputText()]
]

tabs = [
	sg.Tab('Campaign Manager Dynamic Targeting keys', layout_dynamic_targeting_key), 
	sg.Tab('Campaign Manager Resolve Creatives', layout_resolve_creatives)
]

layout = [
	[sg.TabGroup([tabs], tooltip='TIP2')], 
	[sg.Button('Start'), sg.Button('Cancel')]
]  



window = sg.Window('Google Studio / Campaign Manager automatizations', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    print('You entered ', values[0], values[1])

window.close()