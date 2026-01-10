
                #raw f"$say {slot}, {face}, $(chiseled_bookshelf_args)"
execute store success score #ifitem_1 itemio.math if data block ~ ~ ~ Items[{Slot:1b}]
$execute if score #ifitem_1 itemio.math matches 0 run data modify storage itemio:main temp.chiseled_bookshelf_args set value "slot_1_occupied=false,$(chiseled_bookshelf_args)"
$execute if score #ifitem_1 itemio.math matches 1 run data modify storage itemio:main temp.chiseled_bookshelf_args set value "slot_1_occupied=true,$(chiseled_bookshelf_args)"
