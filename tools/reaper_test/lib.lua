-- Banco de pruebas de GenderBender en REAPER (tools/reaper_test). Ver README.md.
-- Un escenario es una lista de acciones que se ejecutan en un bucle defer que termina solo.
-- Resultados en out/: <escenario>.log (PASS/FAIL/SKIP de Lua) y una toma <nombre>.txt por reproduccion.

local src = debug.getinfo(1, "S").source:sub(2)
DIR = src:match("^(.*[/\\])") or "./"
OUT = DIR .. "out/"
reaper.RecursiveCreateDirectory(OUT, 0)

MELO_TEST = "JS: GenderBenderTest/genderbender_melo_test.jsfx"
LOGGER = "JS: GenderBenderTest/gbtest_log.jsfx"
NS_LOG, NS_GUI = "gbtestlog", "gbtestgui"
PROJECT = OUT .. "test_project.rpp"

-- ---------- registro y comprobaciones ----------
local logPath
local counts = {PASS = 0, FAIL = 0, SKIP = 0}
function log(m)
  local f = io.open(logPath or (OUT .. "lib.log"), "a"); f:write(m .. "\n"); f:close()
end
-- ok: true, false o "skip"
function check(name, ok, detail)
  local tag = ok == "skip" and "SKIP" or ok and "PASS" or "FAIL"
  counts[tag] = counts[tag] + 1
  log(string.format("%s %s%s", tag, name, detail and ("  [" .. detail .. "]") or ""))
end
function stopRequested() return reaper.GetExtState("gbtest", "stop") == "1" end

-- ---------- gmem ----------
function G(i) reaper.gmem_attach(NS_GUI); return reaper.gmem_read(i) end
function GW(i, v) reaper.gmem_attach(NS_GUI); reaper.gmem_write(i, v) end

-- ---------- proyecto de prueba ----------
TR = nil
function track(i) return reaper.GetTrack(0, i) end
function setp(n, v) reaper.TrackFX_SetParam(TR, 0, n - 1, v) end
function getp(n) return (reaper.TrackFX_GetParam(TR, 0, n - 1)) end
function P(n) return math.floor(getp(n) + 0.5) end

-- tiempo (s) donde beat_position vale b: beat_position cuenta desde el compas 1 que se ve en la regla,
-- y el proyecto puede empezar antes (medida inicial distinta de 1)
function beatTime(b)
  local txt = reaper.format_timestr_pos(0, "", 2)
  local m0 = tonumber(txt:match("^(-?%d+)")) or 1
  local t1 = reaper.TimeMap2_beatsToTime(0, 0, 1 - m0)
  return reaper.TimeMap2_QNToTime(0, reaper.TimeMap2_timeToQN(0, t1) + b)
end
function beatNow() return reaper.TimeMap2_timeToQN(0, reaper.GetPlayPosition()) - reaper.TimeMap2_timeToQN(0, beatTime(0)) end

local function addFx(tr, name)
  local i = reaper.TrackFX_AddByName(tr, name, false, -1)
  if i < 0 then error("no se encuentra " .. name .. " (instala con: sh tools/install.sh --test)") end
  return i
end

-- abre un proyecto nuevo en otra pestana (el del usuario no se toca) con Melo de prueba y su logger en la pista 1.
-- opts.receivers = n: n pistas receptoras con logger de id 1..n y un envio MIDI desde la pista 1
function setupProject(opts)
  opts = opts or {}
  local _, cur = reaper.EnumProjects(-1)
  if cur == PROJECT then                                -- la pestana de una ejecucion anterior: se guarda y se cierra
    reaper.Main_SaveProjectEx(0, PROJECT, 0)
    reaper.Main_OnCommand(40860, 0)
  end
  reaper.Main_OnCommand(40859, 0)                       -- nueva pestana de proyecto
  for i = reaper.CountTracks(0) - 1, 0, -1 do reaper.DeleteTrack(track(i)) end
  reaper.SetCurrentBPM(0, opts.bpm or 120, false)
  reaper.GetSetRepeat(0)
  reaper.InsertTrackAtIndex(0, false)
  TR = track(0)
  reaper.GetSetMediaTrackInfo_String(TR, "P_NAME", "Melo TEST", true)
  reaper.SetMediaTrackInfo_Value(TR, "I_RECARM", 0)
  addFx(TR, MELO_TEST); addFx(TR, LOGGER)
  for r = 1, opts.receivers or 0 do
    reaper.InsertTrackAtIndex(r, false)
    local rt = track(r)
    reaper.GetSetMediaTrackInfo_String(rt, "P_NAME", "rx " .. r, true)
    reaper.SetMediaTrackInfo_Value(rt, "I_RECARM", 0)
    addFx(rt, LOGGER); reaper.TrackFX_SetParam(rt, 0, 0, r)
    local s = reaper.CreateTrackSend(TR, rt)
    reaper.SetTrackSendInfo_Value(TR, 0, s, "I_SRCCHAN", -1)          -- solo MIDI
  end
  reaper.TrackFX_SetParam(TR, 1, 0, 0)
  reaper.TrackFX_Show(TR, 0, 3)                         -- ventana flotante: @gfx corre y se puede reescalar
  reaper.Main_SaveProjectEx(0, PROJECT, 0)
end

-- filtro de los envios de la pista 1 a las receptoras: "channel" (envio r = canal r) o "bus" (envio r = bus r)
function routeSends(mode)
  for s = 0, reaper.GetTrackNumSends(TR, 0) - 1 do
    reaper.SetTrackSendInfo_Value(TR, 0, s, "I_MIDIFLAGS", mode == "bus" and ((s + 1) << 14) or (s + 1))
  end
end

-- guarda y reabre el proyecto de prueba sin dialogo
function reopenProject()
  reaper.Main_SaveProjectEx(0, PROJECT, 0)
  reaper.Main_openProject("noprompt:" .. PROJECT)
  TR = track(0)
  reaper.TrackFX_Show(TR, 0, 3)
end

-- ---------- estado base y estilos ----------
-- valores por defecto declarados en los sliders de Melo (el clic derecho de la GUI vuelve a estos)
DEFAULTS = {[1]=0,[2]=0,[3]=0,[5]=0,[6]=0,[7]=1,[8]=-1,[9]=0,[10]=0,[11]=30,[12]=0,[13]=0,[14]=0,[15]=50,[16]=1,
  [17]=100,[18]=50,[19]=0,[20]=4,[21]=100,[22]=100,[23]=0,[24]=10,[25]=0,[26]=1,
  [29]=100,[30]=50,[31]=0,[32]=3,[33]=90,[34]=100,[35]=0,[36]=0,[37]=0,[38]=2,[39]=0,[40]=0,
  [41]=100,[42]=50,[43]=0,[44]=3,[45]=100,[46]=100,[47]=0,[48]=40,[49]=0,[50]=3,[51]=12,[53]=0}
-- DEFAULTS con algunos sliders cambiados
function with(t)
  local r = {}
  for k, v in pairs(DEFAULTS) do r[k] = v end
  for k, v in pairs(t or {}) do r[k] = v end
  return r
end

local styleNames
local function loadStyleNames()
  if styleNames then return end
  styleNames = {}
  local f = io.open(reaper.GetResourcePath() .. "/Data/melo_index/estilos.txt")
  if not f then error("falta Data/melo_index/estilos.txt: instala con sh tools/install.sh --test") end
  for l in f:lines() do l = l:gsub("%s+$", ""); if l ~= "" then styleNames[#styleNames + 1] = l end end
  f:close()
end
-- indice de un estilo melodico por nombre (el orden de melo_index/estilos.txt, el mismo que el del slider)
function styleIndex(name)
  loadStyleNames()
  for i, n in ipairs(styleNames) do if n == name then return i - 1 end end
  error("estilo desconocido: " .. name)
end
function styleCount() loadStyleNames(); return #styleNames end

-- trunca temporalmente un estilo instalado (para el aviso de estilo invalido); restoreStyles lo deja como estaba.
-- La copia original queda en out/ hasta restaurarla, asi que un escenario parado tambien la recupera.
local function stylePath(name) return reaper.GetResourcePath() .. "/Data/melo_styles/" .. name .. ".txt" end
function truncateStyle(name)
  local bak = OUT .. "backup_" .. name .. ".txt"
  local f = io.open(stylePath(name), "rb"); local data = f:read("a"); f:close()
  if not reaper.file_exists(bak) then local b = io.open(bak, "wb"); b:write(data); b:close() end
  local t = io.open(stylePath(name), "wb"); t:write(data:sub(1, math.floor(#data * 0.9))); t:close()
end
-- EnumerateFiles guarda el listado en cache: tras borrar un archivo puede seguir devolviendolo,
-- asi que primero se reunen los nombres y se salta el que ya no exista.
function restoreStyles()
  reaper.EnumerateFiles(OUT, -1)                        -- -1 vacia la cache del listado (REAPER 6.20+)
  local names, i = {}, 0
  while true do
    local fn = reaper.EnumerateFiles(OUT, i)
    if not fn then break end
    if fn:match("^backup_(.+)%.txt$") then names[#names + 1] = fn end
    i = i + 1
  end
  for _, fn in ipairs(names) do
    local b = io.open(OUT .. fn, "rb")
    if b then
      local data = b:read("a"); b:close()
      local t = io.open(stylePath(fn:match("^backup_(.+)%.txt$")), "wb"); t:write(data); t:close()
      os.remove(OUT .. fn)
    end
  end
end

-- ---------- base64 (para tocar el estado serializado de un .rpp) ----------
local B64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
function b64dec(s)
  s = s:gsub("[^%w%+/=]", "")
  return (s:gsub(".", function(x)
    if x == "=" then return "" end
    local r, f = "", (B64:find(x, 1, true) - 1)
    for i = 6, 1, -1 do r = r .. (f % 2 ^ i - f % 2 ^ (i - 1) > 0 and "1" or "0") end
    return r
  end):gsub("%d%d%d?%d?%d?%d?%d?%d?", function(x)
    if #x ~= 8 then return "" end
    local c = 0
    for i = 1, 8 do c = c + (x:sub(i, i) == "1" and 2 ^ (8 - i) or 0) end
    return string.char(c)
  end))
end
function b64enc(data)
  return ((data:gsub(".", function(x)
    local r, b = "", x:byte()
    for i = 8, 1, -1 do r = r .. (b % 2 ^ i - b % 2 ^ (i - 1) > 0 and "1" or "0") end
    return r
  end) .. "0000"):gsub("%d%d%d?%d?%d?%d?", function(x)
    if #x < 6 then return "" end
    local c = 0
    for i = 1, 6 do c = c + (x:sub(i, i) == "1" and 2 ^ (6 - i) or 0) end
    return B64:sub(c + 1, c + 1)
  end) .. ({"", "==", "="})[#data % 3 + 1])
end

-- ---------- tomas ----------
LOG_ZONE, LOG_IDS = 200000, 10       -- cada logger escribe en su zona: id * LOG_ZONE
function clearLog()
  reaper.gmem_attach(NS_LOG)
  for id = 0, LOG_IDS - 1 do reaper.gmem_write(id * LOG_ZONE, 0) end
end
-- vuelca la toma: los eventos de cada logger en su orden de emision, logger por logger
function dumpTake(name)
  reaper.gmem_attach(NS_LOG)
  local f, total = io.open(OUT .. name .. ".txt", "w"), 0
  for id = 0, LOG_IDS - 1 do
    local z = id * LOG_ZONE
    local n = math.floor(reaper.gmem_read(z))
    total = total + n
    for i = 0, n - 1 do
      local b = z + 1 + i * 5
      local st = math.floor(reaper.gmem_read(b + 1))
      local d1, d2 = reaper.gmem_read(b + 2), reaper.gmem_read(b + 3)
      local ty = st & 0xF0
      local k = (ty == 0x90 and d2 > 0) and 1 or (ty == 0x80 or ty == 0x90) and 0 or ty == 0xB0 and 2 or -1
      if k >= 0 then
        f:write(string.format("%.6f %d %d %d %d %d\n", reaper.gmem_read(b), k, (st & 15) + 1, d1, d2, reaper.gmem_read(b + 4)))
      end
    end
  end
  f:close()
  return total
end

-- ---------- acciones ----------
-- {"do", fn}  {"set", {[slider] = valor}}  {"take", nombre, desde_beat, hasta_beat, act = fn(beat, f), dur = s}
-- {"wait", fotogramas}  {"click", x, y}  {"rclick", x, y}  {"drag", x0, y0, x1, y1}  {"menu", opcion}
-- {"until", fn, timeout_s, etiqueta}  {"check", nombre, fn -> ok, detalle}  {"reopen"}
-- Cualquier accion admite when = fn: si devuelve false, la accion se salta (p. ej. sin js_ReaScriptAPI).
-- nogui = true en "wait" o "click": se espera que la ventana este cerrada. El fallo por tiempo de la accion
-- sale entonces como PASS y el escenario sigue (comprueba la defensa sin cortar el escenario).
-- Las coordenadas de la GUI van en unidades de 900x540; el plugin las convierte con su escala.
function hx(x, w, lo, hi, v) return x + (v - lo) / (hi - lo) * w end

local function expand(acts)
  local q = {}
  local function push(a) q[#q + 1] = a end
  for _, a in ipairs(acts) do
    -- pasos {x, y, mouse_cap, fotogramas}: el plugin los consume seguidos desde la cola de gmem
    if a[1] == "click" or a[1] == "rclick" then
      local cap = a[1] == "click" and 1 or 2
      push({"mouse", {{a[2], a[3], 0, 2}, {a[2], a[3], cap, 2}, {a[2], a[3], 0, 2}}, when = a.when, nogui = a.nogui})
    elseif a[1] == "drag" then
      push({"mouse", {{a[2], a[3], 0, 2}, {a[2], a[3], 1, 2}, {a[4], a[5], 1, 3}, {a[4], a[5], 0, 2}}, when = a.when, nogui = a.nogui})
    else push(a) end
  end
  return q
end

function runScenario(name, acts)
  logPath = OUT .. name .. ".log"
  local f = io.open(logPath, "w"); f:write(""); f:close()
  reaper.SetExtState("gbtest", "stop", "0", false)
  reaper.SetExtState("gbtest", "state", "running " .. name, false)
  local q = expand(acts)
  local i, st, t0, f0, p0 = 1, nil, 0, 0, 0
  local function finish(why)
    reaper.Main_OnCommand(1016, 0)
    restoreStyles()
    log(string.format("DONE %s: %d PASS, %d FAIL, %d SKIP%s", name, counts.PASS, counts.FAIL, counts.SKIP, why and (" (" .. why .. ")") or ""))
    reaper.SetExtState("gbtest", "state", "done " .. name, false)
  end
  -- la GUI no ha dibujado en 5 s: FAIL y fin, o PASS si la accion lo esperaba (nogui). true = escenario cortado
  local function noGui(a)
    local msg = "la ventana del plugin no dibuja (cerrada o minimizada)"
    if a.nogui then GW(0, 0); check("sin GUI: la accion falla en vez de esperar", true, msg); a.failed = true; return false end
    check("la GUI dibuja", false, msg); finish("sin GUI"); return true
  end
  local function tick()
    if stopRequested() then finish("parado"); return end
    local a = q[i]
    if not a then finish(); return end
    local done, now = false, reaper.time_precise()
    local kind = a[1]
    if not st and a.when and not a.when() then done = true
    elseif kind == "do" then a[2](); done = true
    elseif kind == "set" then for n, v in pairs(a[2]) do setp(n, v) end; done = true
    elseif kind == "menu" then GW(4, a[2]); done = true
    elseif kind == "reopen" then reopenProject(); done = true
    elseif kind == "check" then local ok, d = a[3](); check(a[2], ok, d); done = true
    elseif kind == "mouse" then
      if not st then
        GW(0, 0); GW(6, 0)
        for k, p in ipairs(a[2]) do for j = 1, 4 do GW(100 + (k - 1) * 4 + j - 1, p[j]) end end
        GW(0, #a[2])                                    -- el ultimo: el plugin no empieza hasta tener la cola entera
        st = {}; t0 = now
      elseif G(0) <= 0 then done = true
      elseif now - t0 > 5 then if noGui(a) then return end; done = true end
    elseif kind == "wait" then
      if not st then st = {}; f0 = G(9); t0 = now
      elseif G(9) - f0 >= a[2] then done = true
      elseif now - t0 > 5 then if noGui(a) then return end; done = true end
    elseif kind == "until" then
      if not st then st = {}; t0 = now end
      if a[2]() then done = true
      elseif now - t0 > (a[3] or 10) then check("espera: " .. (a[4] or "?"), false, "tiempo agotado"); done = true end
    elseif kind == "take" then
      if not st then
        reaper.Main_OnCommand(1016, 0)
        reaper.SetEditCurPos(beatTime(a[3]), false, false)
        st = {phase = "settle", n = 0, fired = {}}
      elseif st.phase == "settle" then
        st.n = st.n + 1
        if st.n > 8 then
          clearLog()
          reaper.Main_OnCommand(1007, 0)
          st.phase = "play"; t0 = now; p0 = reaper.GetPlayPosition()
        end
      elseif st.phase == "play" then
        local playing = reaper.GetPlayState() & 1 == 1
        if a.act then a.act(beatNow(), st.fired) end
        if not playing and now - t0 > 1 or (now - t0 > 3 and reaper.GetPlayPosition() == p0) then
          check("el transporte avanza", false, "no se mueve: abre el dispositivo de audio de REAPER"); finish("transporte parado"); return
        end
        if (a.dur and now - t0 >= a.dur) or (not a.dur and beatNow() >= a[4]) then
          reaper.Main_OnCommand(1016, 0); st.phase = "dump"; st.n = 0
        end
      elseif st.phase == "dump" then
        st.n = st.n + 1
        if st.n > 10 then log(string.format("TAKE %s %d eventos", a[2], dumpTake(a[2]))); done = true end
      end
    end
    if done and a.nogui and not a.failed and (kind == "mouse" or kind == "wait") then
      check("sin GUI: la accion falla en vez de esperar", false, "la ventana sigue dibujando")
    end
    if done then i = i + 1; st = nil end
    reaper.defer(tick)
  end
  reaper.defer(tick)
end
