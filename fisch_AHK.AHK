toggled := false

f::
  toggled := !toggled

  Send, {\}
  Sleep, 20

  if (toggled) {
    SetTimer, ClickShake, 20
  } else {
    SetTimer, ClickShake, Off
  }

  ClickShake() {
    Send, {s}
    Sleep, 10
    Send, {Enter}
    Sleep, 10
  }
return
