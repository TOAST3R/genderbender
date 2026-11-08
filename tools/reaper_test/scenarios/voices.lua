-- Voces: BASE del bajo, strum, peso de pad 0 con el pad en una esquina, quinta sobre iv y voice leading,
-- tumbao y swing, rejilla de tresillos, tiempos fuertes y final de la frase B.
local ACID, CUM, SON, BUL = styleIndex("ACID HOUSE"), styleIndex("CUMBIA COLOMBIANA"), styleIndex("SON"), styleIndex("BULERIA")
local function all(i, t) local r = {[1]=i,[2]=i,[3]=i} for k, v in pairs(t or {}) do r[k] = v end return with(r) end
return {
  {"do", function() setupProject() end},
  {"set", all(ACID, {[39]=20})},                         {"take", "v_acid", 0, 16},
  {"set", all(ACID, {[17]=0, [5]=100, [6]=100})},        {"take", "v_pad0", 0, 16},
  {"set", all(CUM)},                                     {"take", "v_cumbia", 0, 16},
  {"set", all(SON)},                                     {"take", "v_son", 0, 8},
  {"set", all(SON, {[15]=66})},                          {"take", "v_son_swing", 0, 8},
  {"set", all(BUL)},                                     {"take", "v_buleria", 0, 32},
}
