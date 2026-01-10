
#loading ioconfig

execute if entity @s[type=marker] run function itemio:v1.5.3/container/input/custom/ioconfig_storage with entity @s data.itemio

execute if entity @s[type=#itemio:item_frames] run function itemio:v1.5.3/container/input/custom/ioconfig_storage with entity @s Item.components."minecraft:custom_data".itemio

execute if entity @s[type=armor_stand] run function itemio:v1.5.3/container/input/custom/ioconfig_storage with entity @s equipment.head.components."minecraft:custom_data".itemio

execute if entity @s[type=#itemio:item_display] run function itemio:v1.5.3/container/input/custom/ioconfig_storage with entity @s item.components."minecraft:custom_data".itemio
