data remove storage itemio:main.input Items
data modify storage itemio:main.input Items set from block ~ ~ ~ Items
data remove storage itemio:main.input Items[{components: {"minecraft:custom_data": {itemio: {gui: 1b}}}}]
data remove storage itemio:main.input input
data modify storage itemio:main.input input set from storage itemio:io input
execute store result score #block_stack itemio.math.input if data storage itemio:main.input Items[]
scoreboard players set #full_stack itemio.math.input 64
data modify entity 93682a08-d099-4e8f-a4a6-1e33a3692301 HandItems[0] set from storage itemio:main.input input
execute as 93682a08-d099-4e8f-a4a6-1e33a3692301 store result score #full_stack itemio.math.input run function itemio:v1.2.6/utils/get_stack_size
execute store result score #count_input itemio.math.input run data get storage itemio:main.input input.count
scoreboard players operation #needed_stack itemio.math.input = #count_input itemio.math.input
scoreboard players operation #needed_stack itemio.math.input /= #full_stack itemio.math.input
scoreboard players add #needed_stack itemio.math.input 1
scoreboard players operation #needed_stack itemio.math.input += #block_stack itemio.math.input
execute if score #needed_stack itemio.math.input <= #block_size itemio.math.input run function itemio:v1.2.6/container/input/vanilla/inf_insert
execute if score #needed_stack itemio.math.input > #block_size itemio.math.input run function itemio:v1.2.6/container/input/vanilla/sup_insert
