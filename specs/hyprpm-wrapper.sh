#!/bin/sh
# hyprpm wrapper for Enterprise Linux.
#  - Hyprland plugins require a C++26 compiler. The EL system GCC is too old,
#    so enable gcc-toolset-15 for hyprpm and the plugin builds it runs.
#  - Hyprland's headers include <lua.h> (Lua 5.5) but hyprland.pc does not declare
#    Lua. On EL, Lua 5.5 lives in /usr/include/lua5.5 (next to the system Lua 5.4),
#    so put it on the compiler include path.
if [ -r /usr/lib/gcc-toolset/15-env.source ]; then
    . /usr/lib/gcc-toolset/15-env.source
fi
CPATH=/usr/include/lua5.5${CPATH:+:$CPATH}
export CPATH
exec /usr/libexec/hyprland/hyprpm "$@"
