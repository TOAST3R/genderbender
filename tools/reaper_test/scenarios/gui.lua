-- GUI: aviso de estilo invalido, indicador de progresion y cambio pendiente, pad, deslizadores (arrastre y
-- clic derecho), botones, menus, reescalado de la ventana, dados y la defensa contra la ventana cerrada.
-- Coordenadas en unidades de la GUI (900x540), sacadas de @gfx de genderbender_melo.jsfx.
-- El indicador se muestrea durante la toma g_ind en out/g_ind.csv; analyze.py lo compara con el estilo.
local BUL, CUM = styleIndex("BULERIA"), styleIndex("CUMBIA COLOMBIANA")
local function all(i, t) local r = {[1]=i,[2]=i,[3]=i} for k, v in pairs(t or {}) do r[k] = v end return with(r) end
local function fmt(t) return table.concat(t, " ") end
local st = {}

-- filas por voz: y del deslizador, centro x de cada columna (fila 1 y fila 2)
local function rowY(v) return 370 + v * 54 + 8 end
local COL1 = {pad = 145, dens = 261, oct = 362, dur = 458, vel = 564, evol = 670}
local COL2 = {swing = 145, slide = 261, canal = 362, extra = 458}
local OFF1 = {pad = 0, dens = 1, oct = 2, dur = 3, vel = 4, evol = 7}
local OFF2 = {swing = 5, slide = 6, canal = 9, extra = 10}

-- sliders de las filas por voz con valores distintos del defecto, para que el clic derecho tenga que cambiarlos
local function scramble()
  local t = {}
  for v = 0, 2 do
    local b = 17 + v * 12
    t[b] = 37; t[b + 1] = 123; t[b + 2] = 1; t[b + 3] = 20; t[b + 4] = 55; t[b + 5] = 33; t[b + 6] = 12
    t[b + 7] = 77; t[b + 9] = 9; t[b + 10] = v == 2 and 20 or 30
  end
  return with(t)
end
local function rclickRows()
  local a = {}
  for v = 0, 2 do
    for k, x in pairs(COL1) do a[#a + 1] = {"rclick", x, rowY(v)} end
    for k, x in pairs(COL2) do
      if k ~= "extra" or v > 0 then a[#a + 1] = {"rclick", x, rowY(v) + 20} end
    end
  end
  return a
end
local function checkRows()
  local bad, n = {}, 0
  local names = {"BASS", "CHORDS", "MELODY"}
  for v = 0, 2 do
    local b = 17 + v * 12
    for _, set in ipairs({OFF1, OFF2}) do
      for k, o in pairs(set) do
        if k ~= "extra" or v > 0 then
          n = n + 1
          if P(b + o) ~= DEFAULTS[b + o] then
            bad[#bad + 1] = string.format("%s %s = %d (defecto %d)", names[v + 1], k == "extra" and (v == 1 and "strum" or "salto") or k, P(b + o), DEFAULTS[b + o])
          end
        end
      end
    end
  end
  return #bad == 0, #bad == 0 and (n .. " deslizadores") or table.concat(bad, "; ")
end

-- reescalado: necesita js_ReaScriptAPI para cambiar el tamano de la ventana flotante
local function hasJS() return reaper.JS_Window_Resize ~= nil end
local function resize(w, h)
  local hwnd = reaper.TrackFX_GetFloatingWindow(TR, 0)
  if hwnd then reaper.JS_Window_Resize(hwnd, w, h) end
end

local A = {
  {"do", function() setupProject() end},
  {"set", all(BUL)}, {"wait", 4},

  -- aviso de estilo invalido: solo en la voz cuyo archivo esta truncado
  {"do", function() truncateStyle("CUMBIA COLOMBIANA"); for i = 40, 42 do GW(i, -1) end end},
  {"set", {[1]=CUM}}, {"wait", 4},
  {"check", "aviso: estilo truncado marcado solo en el bajo", function()
    return G(40) == 1 and G(41) == 0 and G(42) == 0, "aviso " .. fmt({G(40), G(41), G(42)}) end},
  {"do", function() restoreStyles() end},
  {"set", {[1]=BUL}}, {"set", {[1]=CUM}}, {"wait", 4},
  {"check", "aviso: desaparece al cargar el archivo bueno", function()
    return G(40) == 0 and G(41) == 0 and G(42) == 0, "aviso " .. fmt({G(40), G(41), G(42)}) end},

  -- indicador y cambio pendiente: progresion 1 -> 2 en el beat 6; el cambio se aplica en el ciclo siguiente
  {"set", all(BUL)},
  {"do", function() st.csv = io.open(OUT .. "g_ind.csv", "w"); st.f = -1 end},
  {"take", "g_ind", 0, 32, act = function(b, f)
    if b >= 6 and not f.p then f.p = true; setp(10, 1) end
    local fr = G(9)
    if fr ~= st.f and b >= 0 then
      st.f = fr
      st.csv:write(string.format("%.4f %d %d %d %d %d %d %d %d\n", b, G(50), G(51), G(52), G(53), G(54), G(55), G(56), G(57)))
    end
  end},
  {"do", function() st.csv:close() end},
  {"wait", 3},
  {"check", "indicador: parado no marca ningun acorde", function() return G(56) == 0, "marcado " .. G(56) end},

  -- pad: arrastre a una esquina (fuera del pad, se limita a 100/100), a un punto interior y clic derecho
  {"drag", 146, 222, 300, 60}, {"wait", 2},
  {"check", "pad: arrastrar fuera lo limita a la esquina", function() return P(5) == 100 and P(6) == 100, fmt({P(5), P(6)}) end},
  {"drag", 146, 222, 81, 287}, {"wait", 2},
  {"check", "pad: arrastre a (-50, -50)", function() return P(5) == -50 and P(6) == -50, fmt({P(5), P(6)}) end},
  {"rclick", 146, 222}, {"wait", 2},
  {"check", "pad: clic derecho vuelve al centro", function() return P(5) == 0 and P(6) == 0, fmt({P(5), P(6)}) end},

  -- deslizadores: arrastre a la mitad, y clic derecho en todos los de las filas por voz
  {"drag", 210, rowY(0), 261, rowY(0)}, {"wait", 2},
  {"check", "deslizador: densidad del bajo a la mitad = 130", function() return P(18) == 130, "densidad " .. P(18) end},
  {"drag", 304, 198, 600, 198}, {"wait", 2},
  {"check", "deslizador: arrastrar mas alla del final da el maximo (tension 100)", function() return P(11) == 100, "tension " .. P(11) end},
  {"rclick", 374, 198}, {"rclick", 396, 230}, {"rclick", 606, 230}, {"wait", 2},
  {"check", "deslizador: clic derecho en tension, swing y semilla", function()
    return P(11) == 30 and P(15) == 50 and P(16) == 1, fmt({P(11), P(15), P(16)}) .. " (defecto 30 50 1)" end},
  {"set", scramble()}, {"wait", 2},
}
for _, a in ipairs(rclickRows()) do A[#A + 1] = a end
local B = {
  {"wait", 2},
  {"check", "deslizador: clic derecho vuelve al defecto de cada voz", checkRows},

  -- botones
  {"set", all(BUL)}, {"wait", 2},
  {"click", 849, 67}, {"wait", 2},
  {"check", "boton: voz maestra acordes -> melodia", function() return P(7) == 2, "maestra " .. P(7) end},
  {"click", 364, 174}, {"click", 364, 174}, {"wait", 2},
  {"check", "boton: modo de progresion fija -> ciclo -> aleatoria", function() return P(9) == 2, "modo " .. P(9) end},
  {"set", {[9]=0, [10]=0}}, {"wait", 2},
  {"click", 508, 174}, {"wait", 2},
  {"check", "boton: > avanza la progresion", function() return P(10) == 1, "progresion " .. P(10) end},
  {"click", 442, 174}, {"click", 442, 174}, {"wait", 2},
  -- de 1, dos veces <: 0 y luego la ultima progresion (distinta de 0 si el estilo tiene mas de una)
  {"check", "boton: < retrocede y da la vuelta a la ultima", function() return P(10) >= 1, "progresion " .. P(10) end},
  {"click", 500, 198}, {"click", 602, 198}, {"click", 705, 198}, {"click", 817, 198}, {"wait", 2},
  {"check", "boton: ritmo armonico, ciclo, modulacion y salida", function()
    return P(12) == 1 and P(13) == 1 and P(14) == 1 and P(53) == 1, fmt({P(12), P(13), P(14), P(53)}) end},
  {"click", 564, rowY(1) + 20}, {"click", 761, rowY(0)}, {"wait", 2},
  {"check", "boton: acordes partidos y lock del bajo", function() return P(40) == 1 and P(25) == 1, fmt({P(40), P(25)}) end},
  {"set", all(BUL)}, {"wait", 2},

  -- menus: estilo de cada voz, tonica y cancelar
  {"do", function() st.m = G(5) end},
  {"menu", CUM + 1}, {"click", 116, 67},
  {"menu", CUM + 1}, {"click", 326, 67},
  {"menu", 3}, {"click", 637, 174},
  {"menu", 0}, {"click", 536, 67}, {"wait", 2},
  {"check", "menu: estilo del bajo y de los acordes, tonica C#, cancelar deja la melodia", function()
    return P(1) == CUM and P(2) == CUM and P(3) == BUL and P(8) == 1 and G(5) - st.m == 4,
      string.format("estilos %d %d %d, tonica %d, %d menus abiertos", P(1), P(2), P(3), P(8), G(5) - st.m) end},
  {"menu", 1}, {"click", 637, 174}, {"menu", 0}, {"wait", 2},
  {"check", "menu: 'del estilo' vuelve a la tonica del estilo", function() return P(8) == -1, "tonica " .. P(8) end},

  -- reescalado (js_ReaScriptAPI)
  {"do", function()
    if not hasJS() then check("reescalado", "skip", "falta js_ReaScriptAPI"); return end
    st.w, st.h = G(23), G(24)
    resize(1500, 760)
  end},
  {"wait", 4, when = hasJS},
  {"check", "reescalado: la GUI se escala y cabe en la ventana", function()
    local sc = math.min(G(23) / 900, G(24) / 540)
    return G(23) > st.w and math.abs(G(20) - sc) < 0.01 and G(25) == 1,
      string.format("ventana %dx%d, escala %.3f (esperada %.3f), cabe %d", G(23), G(24), G(20), sc, G(25)) end, when = hasJS},
  {"set", {[9]=0, [10]=0}, when = hasJS},
  {"click", 508, 174, when = hasJS}, {"wait", 2, when = hasJS},
  {"check", "reescalado: el boton > funciona igual", function() return P(10) == 1, "progresion " .. P(10) end, when = hasJS},
  {"drag", 146, 222, 81, 287, when = hasJS}, {"wait", 2, when = hasJS},
  {"check", "reescalado: el pad da los mismos valores", function() return P(5) == -50 and P(6) == -50, fmt({P(5), P(6)}) end, when = hasJS},
  {"do", function() resize(math.floor(st.w), math.floor(st.h)) end, when = hasJS},
  {"wait", 4, when = hasJS},

  -- dados
  {"set", with({[1]=0, [2]=1, [3]=2, [16]=5})}, {"wait", 2},
  {"do", function() st.d = {G(34), G(33), P(10)} end},
  {"click", 688, 67}, {"wait", 2},
  {"check", "dado: ALL RND pone el mismo estilo en las tres voces y tira la progresion", function()
    return P(1) == P(2) and P(2) == P(3) and G(34) - st.d[1] == 2 and G(33) - st.d[2] == 1,
      string.format("estilos %d %d %d, tiradas %d, salt +%d", P(1), P(2), P(3), G(34) - st.d[1], G(33) - st.d[2]) end},
  {"do", function() st.d = {G(34)} end},
  {"click", 770, 67}, {"wait", 2},
  {"check", "dado: EACH RND tira una vez por voz", function() return G(34) - st.d[1] == 4, "tiradas " .. (G(34) - st.d[1]) end},
  {"do", function() st.d = {G(33), P(10)} end},
  {"click", 561, 174}, {"wait", 2},
  {"check", "dado: dado prog cambia la progresion", function()
    return G(33) - st.d[1] == 1 and (G(57) <= 1 or P(10) ~= st.d[2]), string.format("progresion %d -> %d, salt +%d", st.d[2], P(10), G(33) - st.d[1]) end},
  {"click", 713, 174}, {"wait", 2},
  {"check", "dado: dado tonica elige una tonica", function() return P(8) >= 0 and P(8) <= 11, "tonica " .. P(8) end},
  {"do", function() st.d = {G(30), G(31), G(32)} end},
  {"set", {[25]=1}},
  {"click", 761, rowY(0) + 20}, {"click", 761, rowY(1) + 20}, {"click", 761, rowY(2) + 20}, {"wait", 2},
  {"check", "dado: dado motivo cambia acordes y melodia, no el bajo bloqueado", function()
    local d = {math.floor(G(30) - st.d[1] + 0.5), math.floor(G(31) - st.d[2] + 0.5), math.floor(G(32) - st.d[3] + 0.5)}
    return fmt(d) == "0 1 1", "incrementos " .. fmt(d) end},
  {"do", function() st.s = P(16) end},
  {"click", 756, 230}, {"wait", 2},
  {"check", "boton: semilla +1", function() return P(16) == st.s + 1, string.format("%d -> %d", st.s, P(16)) end},

  -- ventana cerrada: la accion de GUI falla en lugar de esperar o seguir con datos viejos
  {"do", function() reaper.TrackFX_Show(TR, 0, 2) end},
  {"click", 508, 174, nogui = true},
  {"do", function() reaper.TrackFX_Show(TR, 0, 3) end},
}
for _, a in ipairs(B) do A[#A + 1] = a end
return A
