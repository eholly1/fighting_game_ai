# Audio Files Needed for 2D Fighting Game

Please record and place the following audio files in the specified directories:

## Sound Effects (Place in `src/game/audio/sfx/`)

### Combat Sounds
- **`punch_hit.wav`** - Sound when a punch connects with an opponent
- **`punch_miss.wav`** - Sound when a punch is thrown but misses (optional)
- **`kick_hit.wav`** - Sound when a kick connects with an opponent  
- **`kick_miss.wav`** - Sound when a kick is thrown but misses (optional)
- **`block.wav`** - Sound when an attack is blocked
- **`knockback.wav`** - Sound when a character is knocked back by a kick

### Movement Sounds
- **`jump.wav`** - Sound when a character jumps
- **`land.wav`** - Sound when a character lands from a jump
- **`footstep.wav`** - Sound for character movement (optional)

### UI Sounds
- **`menu_select.wav`** - Sound when navigating menu options
- **`menu_confirm.wav`** - Sound when selecting a menu option
- **`game_start.wav`** - Sound when starting a new game
- **`game_over.wav`** - Sound when the game ends

### Special Effects
- **`health_low.wav`** - Sound when health is critically low (optional)
- **`victory.wav`** - Sound when a player wins (optional)

## Background Music (Place in `src/game/audio/music/`)

### Optional Music Files
- **`menu_theme.ogg`** - Background music for the main menu
- **`battle_theme.ogg`** - Background music during fights
- **`victory_theme.ogg`** - Music when a player wins

## Audio Format Recommendations

### For Sound Effects (.wav files):
- **Sample Rate**: 22050 Hz or 44100 Hz
- **Bit Depth**: 16-bit
- **Channels**: Mono or Stereo
- **Duration**: 0.1 - 2.0 seconds for most effects
- **Volume**: Moderate levels (avoid clipping)

### For Music (.ogg files):
- **Sample Rate**: 44100 Hz
- **Bit Depth**: 16-bit
- **Channels**: Stereo
- **Format**: OGG Vorbis (smaller file size than WAV)
- **Duration**: 30 seconds - 3 minutes (loopable)

## Priority Order

If you want to start with the most important sounds first:

1. **High Priority** (Core gameplay):
   - `punch_hit.wav`
   - `kick_hit.wav` 
   - `block.wav`
   - `knockback.wav`

2. **Medium Priority** (UI feedback):
   - `menu_confirm.wav`
   - `game_start.wav`
   - `game_over.wav`

3. **Low Priority** (Polish):
   - `jump.wav`
   - `land.wav`
   - Background music files

## Notes

- The game will work without audio files (it will print messages about missing files)
- You can start with just a few key sounds and add more later
- All file paths are relative to `src/game/audio/`
- The audio system automatically handles volume control and mixing
