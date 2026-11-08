-- @description GenderBender test: para el escenario en marcha
-- Todos los bucles del banco consultan este ExtState y terminan solos (no hace falta relanzar nada).
-- Restaura ademas cualquier estilo que un escenario haya truncado.
local dir = debug.getinfo(1, "S").source:sub(2):match("^(.*[/\\])")
reaper.SetExtState("gbtest", "stop", "1", false)
reaper.SetExtState("gbtest", "state", "stopped", false)
reaper.Main_OnCommand(1016, 0)
dofile(dir .. "lib.lua")
restoreStyles()
reaper.SetExtState("reaper_mcp_script_result", "last_result", "stopped", false)
