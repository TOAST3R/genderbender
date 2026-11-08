-- Armonia: modos de progresion, ritmo armonico, sustituciones, Markov, modulacion, tonica, cambios de voz
-- maestra y de progresion en el limite del ciclo, y los 6 estilos como maestro cruzados con otros dos.
-- analyze.py compara las tomas con las progresiones de los estilos compilados.
local BUL, CUM = styleIndex("BULERIA"), styleIndex("CUMBIA COLOMBIANA")
local function all(i, t) local r = {[1]=i,[2]=i,[3]=i} for k, v in pairs(t or {}) do r[k] = v end return with(r) end
local A = {
  {"do", function() setupProject() end},
  {"set", all(BUL)},                      {"take", "h_fixed", 0, 16},
  {"set", all(BUL, {[9]=1})},             {"take", "h_cycle", 0, 48},
  {"set", all(BUL, {[12]=1})},            {"take", "h_half", 0, 8},
  {"set", all(BUL, {[9]=3, [11]=0})},     {"take", "h_sub0", 0, 16},
  {"set", all(BUL, {[9]=3, [11]=100})},   {"take", "h_sub100", 0, 16},
  {"set", all(BUL, {[9]=4})},             {"take", "h_markov", 0, 48},
  {"set", all(BUL, {[13]=1, [14]=2})},    {"take", "h_mod", 0, 40},
  {"set", all(CUM)},                      {"take", "h_cumbia", 0, 16},
  {"set", all(CUM, {[8]=0})},             {"take", "h_cumbia_C", 0, 16},
  -- voz maestra: acordes (BULERIA) -> bajo (CUMBIA) a mitad del primer ciclo
  {"set", all(BUL, {[1]=CUM})},
  {"take", "h_master", 0, 32, act = function(b, f) if b >= 6 and not f.m then f.m = true; setp(7, 0) end end},
  -- progresion 1 -> 2 a mitad del primer ciclo
  {"set", all(BUL)},
  {"take", "h_prog", 0, 32, act = function(b, f) if b >= 6 and not f.p then f.p = true; setp(10, 1) end end},
}
-- cada estilo como maestro (voz de acordes, Markov), con el bajo y la melodia de otros dos estilos
local n = styleCount()
for m = 0, n - 1 do
  A[#A + 1] = {"set", with({[1]=(m + 1) % n, [2]=m, [3]=(m + 2) % n, [9]=4})}
  A[#A + 1] = {"take", "h_master" .. m, 0, 16}
end
return A
