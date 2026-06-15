# Retro RPG Campaign

**Retro RPG Campaign** is a turn-based role-playing game (RPG) with rogue-like elements, developed in Python using the Pygame library. The project features a modular architecture that strictly separates core business logic (entities), user interface (ui), and the main game state engine (core).

## Gameplay Features

* **Turn-Based Combat System:** Every action requires a tactical decision — attack the enemy or drink a health potion to restore HP. Inputs are strictly locked during enemy turns and animations to maintain a balanced flow.
* **Three-Level Campaign:** Fight your way through a progression of scaling enemies, starting from a level 1 Goblin, moving up to a ferocious Orc Warrior, and concluding with a final Demon Lord Boss fight.
* **Loot & Inventory System:** Defeating enemies rewards the player with random drops — potions or equipment (weapons/armor) with randomized attack and defense stat modifiers.
* **Equipment Management:** An interactive inventory bag (`[I]`) allows players to select and equip found items to instantly upgrade their base attributes.
* **Dynamic Combat Log:** An informative battle text feed equipped with automatic word wrap to handle detailed damage breakdowns without cluttering the screen.

---

## Project Architecture

The project is built around a robust **State/Scene Manager** pattern, allowing for seamless feature scaling and clean separation of concerns:

```text
TestRPGdev/
│
├── assets/                  # Graphical resources (character sprites)
│   ├── player.png
│   ├── goblin.png
│   ├── orc.png
│   └── demon.png
│
├── core/                    # Core game engine and configurations
│   ├── config.py            # Global constants, colors, and system fonts
│   └── game_manager.py      # Main State Controller and game loop coordinator
│
├── entities/                # Core business logic (Backend models)
│   └── character.py         # Character base class, stat scaling, and animation handling
│
├── ui/                      # Visual components and screen layouts
│   ├── combat_log.py        # Battle text feed component with word wrap logic
│   └── scenes.py            # Isolated screen state classes (Battle, Inventory, Loot, etc.)
│
└── main.py                  # Application entry point (Initializes Pygame and starts GameManager)
```

## Installation & Setup for Developers
To run this project from source, you will need Python 3.10+ installed on your machine.

1. Clone the repository or download the source code:

```Bash
git clone (https://github.com/NosykS/Retro-RPG-Campaign)
cd TestRPGdev
```
2. Create and activate a virtual environment:

```Bash
python -m venv .venv
# For Windows:
.venv\Scripts\activate
# For macOS/Linux:
source .venv/bin/activate
```
3. Install the required dependencies:

```Bash
pip install pygame
```
4. Run the game:

```Bash
python main.py
```
## Game Controls
- UP / DOWN Arrow Keys — Navigate through the combat menu options or your inventory items.
- ENTER — Confirm your current selection (Attack, Drink Potion, Equip Item, or Proceed to next level).
- I — Toggle the player's inventory bag open/closed (Available during your turn in battle).
- R — Restart the campaign (Available on the Game Over screen).
- ESC — Instantly quit the game application.

## Building a Standalone Executable (.EXE)
The project is pre-configured for deployment using PyInstaller. Thanks to the integrated dynamic asset path manager (resource_path), all graphical assets are compiled safely into the distribution package.

To bundle the application into a standalone folder that runs on any computer without a Python installation:

1. Install PyInstaller into your active virtual environment:

```Bash
pip install pyinstaller
```
2. Execute the compilation command (for Windows):

```Bash
pyinstaller --noconfirm --onedir --windowed --add-data "assets;assets" main.py
```
3. Your production-ready build will be located in the dist/main/ folder.

4. To distribute the game, compress the main folder into a .ZIP or .RAR archive. The game can be launched by running main.exe from the unzipped directory.