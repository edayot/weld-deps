$execute store success score #if_item itemio.math.input if data storage itemio:main.input Items[{Slot:$(Slot)b}]
execute if score #if_item itemio.math.input matches 0 run function itemio:v1.0.0/container/input/custom/input_no_config/process_input/unless_item with storage itemio:main.input temp.args
execute if score #if_item itemio.math.input matches 1 run function itemio:v1.0.0/container/input/custom/input_no_config/process_input/if_item with storage itemio:main.input temp.args
