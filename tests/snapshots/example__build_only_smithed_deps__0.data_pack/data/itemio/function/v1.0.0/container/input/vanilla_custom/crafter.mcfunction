data remove storage itemio:main.input Items
data modify storage itemio:main.input Items set from block ~ ~ ~ Items
data remove storage itemio:main.input Items[{components: {"minecraft:custom_data": {itemio: {gui: 1b}}}}]
data remove storage itemio:main.input disabled_slots
data modify storage itemio:main.input disabled_slots set from block ~ ~ ~ disabled_slots
data remove storage itemio:main.input input
data modify storage itemio:main.input input set from storage itemio:io input
data modify entity 93682a08-d099-4e8f-a4a6-1e33a3692301 HandItems[0] set from storage itemio:main.input input
execute as 93682a08-d099-4e8f-a4a6-1e33a3692301 store result score #stack_size itemio.math.input run function itemio:v1.0.0/utils/get_stack_size
scoreboard players set #success_input itemio.math.input 0
data modify storage itemio:main.input Items_clean set value []
scoreboard players set #slot_clean itemio.math.input 0
function itemio:v1.0.0/container/input/vanilla_custom/crafter/cleaning {slot_clean: 0}
execute if data storage itemio:main.input disabled_slots[0] if data storage itemio:main.input Items_clean[0] run function itemio:v1.0.0/container/input/vanilla_custom/crafter/delete_disabled
scoreboard players set #max_iteration itemio.math.input 64
execute store result score #count_input itemio.math.input run data get storage itemio:main.input input.count
execute if score #count_input itemio.math.input matches 1.. if data storage itemio:main.input Items_clean[0] run function itemio:v1.0.0/container/input/vanilla_custom/crafter/loop_input
execute if score #success_input itemio.math.input matches 1 run function itemio:v1.0.0/container/input/vanilla_custom/crafter/success
