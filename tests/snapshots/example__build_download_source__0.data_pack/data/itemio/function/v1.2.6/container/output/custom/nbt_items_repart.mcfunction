execute if entity @s[type=marker] run data modify storage itemio:main.output nbt_items_path set from entity @s data.itemio.nbt_items_path
execute if entity @s[type=#itemio:item_frames] run data modify storage itemio:main.output nbt_items_path set from entity @s Item.components."minecraft:custom_data".itemio.nbt_items_path
execute if entity @s[type=armor_stand] run data modify storage itemio:main.output nbt_items_path set from entity @s ArmorItems[3].components."minecraft:custom_data".itemio.nbt_items_path
execute if entity @s[type=#itemio:item_display] run data modify storage itemio:main.output nbt_items_path set from entity @s item.components."minecraft:custom_data".itemio.nbt_items_path
scoreboard players set #nb_entities itemio.math.output 0
execute if entity @s[tag=itemio.container.nbt_items.on_passengers] on passengers run function itemio:v1.2.6/container/output/custom/nbt_items with storage itemio:main.output {}
execute if entity @s[tag=itemio.container.nbt_items.on_vehicle] on vehicle run function itemio:v1.2.6/container/output/custom/nbt_items with storage itemio:main.output {}
execute if entity @s[tag=!itemio.container.nbt_items.on_passengers, tag=!itemio.container.nbt_items.on_vehicle] run function itemio:v1.2.6/container/output/custom/nbt_items with storage itemio:main.output {}
