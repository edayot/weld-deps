
#loading ioconfig
data remove storage itemio:main.input ioconfig

scoreboard players set #ioconfig_from_storage itemio.math.input 0
execute if entity @s[tag=itemio.container.ioconfig_from_storage] run scoreboard players set #ioconfig_from_storage itemio.math.input 1

execute if score #ioconfig_from_storage itemio.math.input matches 0 run function itemio:v1.5.3/container/input/custom/input_normal

execute if score #ioconfig_from_storage itemio.math.input matches 1 run function itemio:v1.5.3/container/input/custom/input_storage

data remove storage itemio:main.input ioconfig[{mode: "output"}]

scoreboard players set #good_context_entity itemio.math.input 1
execute if data storage itemio:main.input ioconfig if data storage itemio:io input run function itemio:v1.5.3/container/input/custom/input_noconfig
scoreboard players set #good_context_entity itemio.math.input 0
