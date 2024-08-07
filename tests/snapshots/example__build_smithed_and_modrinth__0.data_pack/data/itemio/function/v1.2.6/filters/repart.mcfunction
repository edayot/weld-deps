execute if score #filter.valid_item itemio.io matches 1 if data storage itemio:io filter.energy run function itemio:v1.2.6/filters/energy
execute if score #filter.valid_item itemio.io matches 1 if data storage itemio:io filter.id run function itemio:v1.2.6/filters/id
execute if score #filter.valid_item itemio.io matches 1 if data storage itemio:io filter.ctc run function itemio:v1.2.6/filters/ctc
execute if score #filter.valid_item itemio.io matches 1 if data storage itemio:io filter.smithed.id run function itemio:v1.2.6/filters/smithed_id
execute if score #filter.valid_item itemio.io matches 1 if data storage itemio:io filter.merge as 93682a08-d099-4e8f-a4a6-1e33a3692301 run function itemio:v1.2.6/filters/merge
execute if score #filter.valid_item itemio.io matches 1 if data storage itemio:io filter.item_predicate as 93682a08-d099-4e8f-a4a6-1e33a3692301 run function itemio:v1.2.6/filters/item_predicate with storage itemio:io filter
function itemio:v1.2.6/filters/minecraft_tags
