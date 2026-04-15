execute store success score #ifitem_5 itemio.math if data block ~ ~ ~ Items[{Slot:5b}]
$execute if score #ifitem_5 itemio.math matches 0 run data modify storage itemio:main temp.chiseled_bookshelf_args set value "slot_5_occupied=false,$(chiseled_bookshelf_args)"
$execute if score #ifitem_5 itemio.math matches 1 run data modify storage itemio:main temp.chiseled_bookshelf_args set value "slot_5_occupied=true,$(chiseled_bookshelf_args)"
