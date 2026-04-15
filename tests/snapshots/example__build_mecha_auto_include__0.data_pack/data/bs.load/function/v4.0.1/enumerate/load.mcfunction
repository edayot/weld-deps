# ------------------------------------------------------------------------------------------------------------
# Copyright (c) 2026 Gunivers
#
# This file is part of the Bookshelf project (https://github.com/mcbookshelf/bookshelf).
#
# This source code is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Conditions:
# - You may use this file in compliance with the MPL v2.0
# - Any modifications must be documented and disclosed under the same license
#
# For more details, refer to the MPL v2.0.
# ------------------------------------------------------------------------------------------------------------

# Add the version of the module to the list of available modules
data modify storage bs:data load.modules append value {module:"bs.load",version:"4.0.1"}
scoreboard players add $bs.load.major load.status 0
scoreboard players add $bs.load.minor load.status 0
scoreboard players add $bs.load.patch load.status 0

# Count the number of major versions
execute unless score $bs.load.major load.status matches 4 run scoreboard players add #bs.load.major_versions load.status 1

# Set the latest available version for the module
execute unless score $bs.load.major load.status matches ..4 run return 0
execute if score $bs.load.major load.status matches 4 unless score $bs.load.minor load.status matches ..0 run return 0
execute if score $bs.load.major load.status matches 4 if score $bs.load.minor load.status matches 0 unless score $bs.load.patch load.status matches ..1 run return 0
scoreboard players set $bs.load.major load.status 4
scoreboard players set $bs.load.minor load.status 0
scoreboard players set $bs.load.patch load.status 1
