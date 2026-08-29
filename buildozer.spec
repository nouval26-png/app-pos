[app]

# (str) Title of your application
title = Toko Humaira POS

# (str) Package name
package.name = tokohumaira

# (str) Package domain (needed for android packaging)
package.domain = org.pos

# (str) Source files where the let's go
source.dir = .

# (list) Source files to include (let's include all)
source.include_exts = py,png,jpg,kv,atlas

# (list) Application requirements
# comma separated e.g. requirements = kivy,somesql
requirements = python3,kivy

# (str) Supported orientations
orientation = portrait

# (int) Selscreen (0 = no, 1 = yes)
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET
