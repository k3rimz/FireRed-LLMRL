-- Initialize socket library
local socket = require("socket")

-- Button mapping
local buttons = {
    up = "Up",
    down = "Down",
    left = "Left",
    right = "Right",
    a = "A",
    b = "B",
    start = "Start",
    select = "Select"
}


-- Create UDP client and connect to Python server
local client = socket.udp()
client:setpeername("127.0.0.1", 65432)
client:settimeout(0)  -- Non-blocking

-- Send initial ready signal
console.log("Sending ready signal to Python server")
client:send("ready")

-- Main loop
while true do
    -- Handle incoming commands
    local data = client:receive()
    if data then
        local cmd = data:match("^(%S+)")
        
        if cmd == "press" then
            -- Handle button press
            local button, duration = data:match("press (%S+) (%S+)")
            if button and buttons[button] then
                -- Create joypad table
                local controls = {}
                for b in pairs(buttons) do
                    controls[buttons[b]] = (b == button)
                end
                
                -- Press button for duration
                local frames = math.floor(duration * 60)  -- Convert seconds to frames
                for i=1,frames do
                    joypad.set(controls, 1)
                    emu.frameadvance()
                end
                
                -- Release button
                for b in pairs(buttons) do
                    controls[buttons[b]] = false
                end
                joypad.set(controls, 1)
                
                client:send("ok")
            end
            
        elseif cmd == "screen" then
            -- Capture and send screen content
            local pixels = client.screenshottoclipboard()
            client:send(pixels)
            
        elseif cmd == "loadstate" then
            -- Load save state
            local path = data:match("loadstate (.+)")
            if path then
                savestate.load(path)
                client:send("ok")
            else
                client:send("error: invalid path")
            end
            
        elseif cmd == "exit" then
            break
        end
    end
    
    -- Advance emulation
    emu.frameadvance()
end

-- Cleanup
if client then
    client:close()
end