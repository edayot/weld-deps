$execute store result storage itemio:main.input Items[{Slot:$(Slot)b}].count int 1 run scoreboard players get #full_stack itemio.math.input
$execute if score #nbt_items itemio.math.input matches 0 store result block ~ ~ ~ Items[{Slot:$(Slot)b}].count int 1 run scoreboard players get #full_stack itemio.math.input
execute if score #nbt_items itemio.math.input matches 1 run function itemio:v1.0.0/container/input/custom/input_no_config/process_input/if_item/sup/fill/nbt_items with storage itemio:main.input temp.args
scoreboard players set #new_count_input itemio.math.input 0
scoreboard players operation #new_count_input itemio.math.input = #new_count_container itemio.math.input
scoreboard players operation #new_count_input itemio.math.input -= #full_stack itemio.math.input
execute store result storage itemio:main.input input.count int 1 run scoreboard players get #new_count_input itemio.math.input
scoreboard players set #success_input itemio.io 1
