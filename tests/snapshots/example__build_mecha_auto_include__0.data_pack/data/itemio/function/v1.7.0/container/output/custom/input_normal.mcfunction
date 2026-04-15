
#loading ioconfig

execute if entity @s[type=marker] run data modify storage itemio:main.output ioconfig set from entity @s data.itemio.ioconfig

execute if entity @s[type=#itemio:item_frames] run data modify storage itemio:main.output ioconfig set from entity @s Item.components."minecraft:custom_data".itemio.ioconfig

execute if entity @s[type=armor_stand] run data modify storage itemio:main.output ioconfig set from entity @s equipment.head.components."minecraft:custom_data".itemio.ioconfig

execute if entity @s[type=#itemio:item_display] run data modify storage itemio:main.output ioconfig set from entity @s item.components."minecraft:custom_data".itemio.ioconfig
