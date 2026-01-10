
$execute if score #nbt_items itemio.math.input matches 0 run item modify block ~ ~ ~ container.$(Slot) itemio:v1.5.3/internal/input/add_count

execute if score #nbt_items itemio.math.input matches 1 run function itemio:v1.5.3/container/input/custom/input_no_config/process_input/if_item/inf/fill/nbt_items with storage itemio:main.input temp.args

scoreboard players set #success_input itemio.io 1
data modify storage itemio:main.input input.count set value 0b
