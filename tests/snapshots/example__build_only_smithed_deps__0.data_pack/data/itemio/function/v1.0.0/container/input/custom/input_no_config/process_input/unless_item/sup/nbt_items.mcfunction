$execute if entity @s[tag=itemio.container.nbt_items.on_passengers] on passengers run data modify $(nbt_items_path) append from storage itemio:main.input input
$execute if entity @s[tag=itemio.container.nbt_items.on_vehicle] on vehicle run data modify $(nbt_items_path) append from storage itemio:main.input input
$execute if entity @s[tag=!itemio.container.nbt_items.on_vehicle,tag=!itemio.container.nbt_items.on_passengers] run data modify $(nbt_items_path) append from storage itemio:main.input input
