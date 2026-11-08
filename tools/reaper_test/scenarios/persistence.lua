-- Persistencia: semilla, recarga del plugin, lock al reabrir, dados (pulsados en la GUI) al reabrir
-- y un proyecto con el formato de @serialize anterior a los indices de estilo.
local BUL = styleIndex("BULERIA")
local function all(i, t) local r = {[1]=i,[2]=i,[3]=i} for k, v in pairs(t or {}) do r[k] = v end return with(r) end
local SEED7 = all(BUL, {[16]=7, [9]=4, [5]=60, [6]=-20})
local st = {}

-- enteros: gmem_read da floats ("1.0") y las comparaciones son de texto
local function ser() local t = {} for i = 30, 34 do t[#t + 1] = math.floor(G(i) + 0.5) end return t end
local function clearSer() for i = 30, 34 do GW(i, -1) end; for i = 40, 42 do GW(i, -1) end end
local function fmt(t) return table.concat(t, " ") end

-- copia del proyecto de prueba sin los 3 ultimos valores de @serialize de Melo (el formato anterior)
local function makeOldFormat()
  reaper.Main_SaveProjectEx(0, PROJECT, 0)
  local f = io.open(PROJECT); local t = f:read("a"); f:close()
  local i = t:find("genderbender_melo_test.jsfx", 1, true)
  st.files = {t:match('"([^"]+)%.txt" "([^"]+)%.txt" "([^"]+)%.txt"', i)}
  local _, b = t:find("<JS_SER[^\n]*\n", i)
  local c = t:find("\n%s*>", b)
  local raw = b64dec(t:sub(b + 1, c))
  local v = {}
  for k = 1, #raw // 4 do v[k] = string.unpack("<f", raw, (k - 1) * 4 + 1) end
  st.oldSer = {v[2], v[3], v[4], v[#v - 4], v[#v - 3]}    -- motivos, salt y dados (los 3 ultimos son los estilos)
  local old = raw:sub(1, #raw - 12)
  local o = io.open(OUT .. "old_format.rpp", "w"); o:write(t:sub(1, b) .. b64enc(old) .. t:sub(c)); o:close()
end

return {
  {"do", function() setupProject() end},
  {"set", all(BUL)},                                    {"take", "p_fixed", 0, 16},
  {"set", SEED7},                                       {"take", "p_seed7a", 0, 16},
                                                        {"take", "p_seed7b", 0, 16},
  {"set", all(BUL, {[16]=8, [9]=4, [5]=60, [6]=-20})}, {"take", "p_seed8", 0, 16},
  -- recarga: quitar el plugin y volver a ponerlo
  {"do", function()
    reaper.TrackFX_Delete(TR, 0)
    reaper.TrackFX_AddByName(TR, MELO_TEST, false, -1000)
    reaper.TrackFX_Show(TR, 0, 3)
  end},
  {"set", SEED7},                                       {"take", "p_reload", 0, 16},
  -- lock del bajo en el centro; despues se mueven el pad y la densidad y se reabre el proyecto
  {"set", all(BUL, {[25]=1})},
  {"take", "p_lock", 0, 4, act = function(b, f)
    if b >= 1 and not f.l then f.l = true; setp(5, 100); setp(6, 100); setp(18, 200); setp(30, 200) end end},
  {"reopen"}, {"wait", 6},
  {"check", "lock: el lock, el pad y la densidad se conservan al reabrir", function()
    return P(25) == 1 and P(5) == 100 and P(6) == 100 and P(18) == 200,
      string.format("lock=%d pad=(%d, %d) densidad=%d", P(25), P(5), P(6), P(18)) end},
  {"take", "p_lock_reopen", 0, 16},
  -- dados pulsados en la GUI: EACH RND, dado de motivo de la melodia y dado de progresion
  {"set", with({[1]=0, [2]=1, [3]=2, [9]=4, [16]=3})}, {"wait", 4},
  {"click", 770, 67}, {"wait", 3}, {"click", 761, 506}, {"wait", 2}, {"click", 561, 174}, {"wait", 2},
  {"do", function() st.s = {P(1), P(2), P(3), P(7), P(10)}; st.g = ser() end},
  {"check", "dados: EACH RND cambia los estilos", function()
    return not (st.s[1] == 0 and st.s[2] == 1 and st.s[3] == 2), "estilos " .. fmt({st.s[1], st.s[2], st.s[3]}) end},
  {"take", "p_dice", 0, 16},
  {"reopen"}, {"do", clearSer}, {"wait", 6},
  {"check", "dados: estilos, maestra y progresion se conservan al reabrir", function()
    local g = {P(1), P(2), P(3), P(7), P(10)}
    return fmt(g) == fmt(st.s), fmt(g) .. " (antes " .. fmt(st.s) .. ")" end},
  {"check", "dados: motivos, salt y contador de dados (@serialize) al reabrir", function()
    return fmt(ser()) == fmt(st.g), fmt(ser()) .. " (antes " .. fmt(st.g) .. ")" end},
  {"check", "dados: los tres estilos cargan validos al reabrir", function()
    return G(40) == 0 and G(41) == 0 and G(42) == 0, "aviso " .. fmt({G(40), G(41), G(42)}) end},
  {"take", "p_dice_reopen", 0, 16},
  -- proyecto con el @serialize anterior: estilos por nombre de archivo y el resto del estado igual
  {"do", makeOldFormat},
  {"do", function()
    reaper.Main_openProject("noprompt:" .. OUT .. "old_format.rpp"); TR = track(0); reaper.TrackFX_Show(TR, 0, 3); clearSer()
  end},
  {"wait", 6},
  {"check", "formato anterior: estilos segun los nombres guardados", function()
    local want = {styleIndex(st.files[1]), styleIndex(st.files[2]), styleIndex(st.files[3])}
    return fmt({P(1), P(2), P(3)}) == fmt(want), fmt({P(1), P(2), P(3)}) .. " (archivos " .. table.concat(st.files, ", ") .. ")" end},
  {"check", "formato anterior: motivos, salt y dados se leen igual", function()
    local w = {} for k, x in ipairs(st.oldSer) do w[k] = math.floor(x + 0.5) end
    return fmt(ser()) == fmt(w), fmt(ser()) .. " (archivo " .. fmt(w) .. ")" end},
  {"do", function() reaper.Main_openProject("noprompt:" .. PROJECT); TR = track(0) end},
}
