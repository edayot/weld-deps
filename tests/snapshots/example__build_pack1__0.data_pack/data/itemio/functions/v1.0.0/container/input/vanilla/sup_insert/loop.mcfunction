data remove storage itemio:main.input temp.args
execute store result storage itemio:main.input temp.args.Slot int 1 run scoreboard players get #temp_slot itemio.math.input
data modify storage itemio:main.input temp.args.nbt_items_path set value "storage blbblb:yolo do_not_use"
function itemio:v1.0.0/container/input/custom/input_no_config/process_input with storage itemio:main.input temp.args
scoreboard players add #temp_slot itemio.math.input 1
function itemio:v1.0.0/container/input/if_item_input
execute if score #temp_success_lol itemio.math.input matches 1 if score #temp_slot itemio.math.input < #block_size itemio.math.input run function itemio:v1.0.0/container/input/vanilla/sup_insert/loop
