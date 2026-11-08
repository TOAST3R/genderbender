-- @description GenderBender test: lanza el escenario que da nombre al archivo (run_<escenario>.lua)
-- install.sh --test copia este archivo como run_<escenario>.lua por cada archivo de scenarios/.
-- El resultado (para el MCP de REAPER) dice donde queda el registro; el escenario sigue en segundo plano.
local src = debug.getinfo(1, "S").source:sub(2)
local dir = src:match("^(.*[/\\])")
local name = src:match("run_([%w_]+)%.lua$")
local ok, err = pcall(function()
  if not name then error("el lanzador tiene que llamarse run_<escenario>.lua") end
  dofile(dir .. "lib.lua")
  if reaper.GetExtState("gbtest", "state"):match("^running") and reaper.GetExtState("gbtest", "stop") ~= "1" then
    error("ya hay un escenario en marcha: espera a que termine o lanza stop.lua")
  end
  runScenario(name, dofile(dir .. "scenarios/" .. name .. ".lua"))
end)
reaper.SetExtState("reaper_mcp_script_result", "last_result",
  ok and ("started " .. name .. " -> " .. dir .. "out/" .. name .. ".log") or ("error: " .. tostring(err)), false)
