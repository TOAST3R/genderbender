-- Salida MIDI: slide y CC 65, enrutado por canal y por bus a pistas receptoras, acordes partidos,
-- seek, loop y cambio de destino. Las comprobaciones de notas las hace analyze.py sobre las tomas.
local BUL, ACID = styleIndex("BULERIA"), styleIndex("ACID HOUSE")
local function bul(t) local r = {[1]=BUL,[2]=BUL,[3]=BUL} for k, v in pairs(t or {}) do r[k] = v end return with(r) end
return {
  {"do", function() setupProject({receivers = 3}) end},
  {"set", with({[1]=ACID,[2]=ACID,[3]=ACID})}, {"take", "o_slide", 0, 16},
  {"do", function() routeSends("channel") end},
  {"set", bul()}, {"take", "o_chan", 0, 8},
  {"do", function() routeSends("bus") end},
  {"set", bul({[53]=1})}, {"take", "o_bus", 0, 8},
  -- acordes partidos: la melodia va al destino 8 para no pisar las notas del acorde (2, 3, 4, 5)
  {"set", bul({[53]=1, [40]=1, [50]=8})}, {"take", "o_split", 0, 8},
  {"do", function() routeSends("channel") end},
  {"set", bul()},
  {"take", "o_seek", 0, 24, act = function(b, f)
    if b >= 6 and not f.s then f.s = true; reaper.SetEditCurPos(beatTime(18), true, true) end end},
  {"take", "o_loop", 0, 999, dur = 9, act = function(b, f)
    if not f.l then f.l = true; reaper.GetSet_LoopTimeRange(true, true, beatTime(0), beatTime(6), false); reaper.GetSetRepeat(1) end end},
  {"do", function() reaper.GetSetRepeat(0); reaper.GetSet_LoopTimeRange(true, true, 0, 0, false) end},
  {"take", "o_dest", 0, 16, act = function(b, f) if b >= 6 and not f.d then f.d = true; setp(26, 5) end end},
}
