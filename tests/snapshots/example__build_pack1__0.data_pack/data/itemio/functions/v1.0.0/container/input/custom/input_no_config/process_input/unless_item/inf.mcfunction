execute if score #nbt_items itemio.math.input matches 0 run data modify block ~ ~ ~ Items append from storage itemio:main.input input
execute if score #nbt_items itemio.math.input matches 1 run function itemio:v1.0.0/container/input/custom/input_no_config/process_input/unless_item/inf/nbt_items with storage itemio:main.input temp.args
data modify storage itemio:main.input input.count set value 0b
