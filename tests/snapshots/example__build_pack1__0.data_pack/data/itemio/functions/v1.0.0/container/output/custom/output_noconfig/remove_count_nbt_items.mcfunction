data modify storage itemio:main.output temp.args_check_filters.nbt_items_path set from storage itemio:main.output nbt_items_path
execute if entity @s[tag=itemio.container.nbt_items.on_passengers] on passengers run function itemio:v1.0.0/container/output/custom/output_noconfig/real_remove_count_nbt_items with storage itemio:main.output temp.args_check_filters
execute if entity @s[tag=itemio.container.nbt_items.on_vehicle] on vehicle run function itemio:v1.0.0/container/output/custom/output_noconfig/real_remove_count_nbt_items with storage itemio:main.output temp.args_check_filters
execute if entity @s[tag=!itemio.container.nbt_items.on_passengers, tag=!itemio.container.nbt_items.on_vehicle] run function itemio:v1.0.0/container/output/custom/output_noconfig/real_remove_count_nbt_items with storage itemio:main.output temp.args_check_filters
